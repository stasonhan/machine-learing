from plane import planemunk
import numpy as np
import random
import csv
from nn import neural_net,LossHistory
import os.path
import timeit


NUM_INPUT = 3
GAMMA = 0.9 
TUNING = False

def train_net(model,params):
    """
    model:
    """
    file_name = params_to_filename(params)
    observe = 1000
    epsilon = 1
    train_frames = 1000000
    batchSize = params['batchSize']
    buffer = params['buffer']
    
    max_plane_distance = 0
    plane_distance=0
    
    t = 0
    data_collect = []
    replay = []
    loss_log=[]
    plane_state = planemunk.Demo()
    plane_state.set_target(1900, 1060,50) #set the target to reach
    _,state,_ = plane_state.frame_step((2))
    
    start_time = timeit.default_timer()
    while t < train_frames:
        t += 1
        plane_distance += 1
        if random.random() < epsilon or t < observe:
            action = np.random.randint(0,3)
            
        else:
            qval=model.predict(state,batch_size = 1)
            action = (np.argmax(qval))
        reward,new_state,target = plane_state.frame_step(action)
        if target:
            plane_state.reset()
            plane_state.set_target(1900, 1060,50)
        replay.append((state,action,reward,new_state))
        if t > observe:
            if len(replay) > buffer:
                replay.pop(0)
            minibatch = random.sample(replay, batchSize)
            X_train, y_train = process_minibatch(minibatch, model)
            
            history = LossHistory()
            model.fit(
                X_train, y_train, batch_size=batchSize,
                nb_epoch=1, verbose=0, callbacks=[history]
                )
            loss_log.append(history.losses)
            
        state = new_state
        if epsilon > 0.1 and t > observe:
            epsilon -= (1/train_frames)
            
        if reward == -500:
            data_collect.append([t,plane_distance])
            if plane_distance > max_plane_distance:
                max_plane_distance = plane_distance
            tot_time = timeit.default_timer() - start_time
            fps = plane_distance / tot_time
            print(("Max: %d at %d\tepsilon %f\t(%d)\t%f fps" %
                   (max_plane_distance, t, epsilon, plane_distance, fps)))
            # Reset.
            plane_distance = 0
            start_time = timeit.default_timer()

        # Save the model every 25,000 frames.
        if t % 500 == 0:
            model.save_weights('saved-models/' + file_name + '-' +
                               str(t) + '.h5',
                               overwrite=True)
            print(("Saving model %s - %d" % (file_name, t)))

    # Log results after we're done all frames.
    log_results(file_name, data_collect, loss_log)  
    
def log_results(filename, data_collect, loss_log):
    # Save the results to a file so we can graph it later.
    with open('results/sonar-frames/learn_data-' + filename + '.csv', 'w') as data_dump:
        wr = csv.writer(data_dump)
        wr.writerows(data_collect)

    with open('results/sonar-frames/loss_data-' + filename + '.csv', 'w') as lf:
        wr = csv.writer(lf)
        for loss_item in loss_log:
            wr.writerow(loss_item)


def process_minibatch(minibatch, model):
    """This does the heavy lifting, aka, the training. It's super jacked."""
    X_train = []
    y_train = []
    # Loop through our batch and create arrays for X and y
    # so that we can fit our model at every step.
    for memory in minibatch:
        # Get stored values.
        old_state_m, action_m, reward_m, new_state_m = memory
        # Get prediction on old state.
        old_qval = model.predict(old_state_m, batch_size=1)
        # Get prediction on new state.
        newQ = model.predict(new_state_m, batch_size=1)
        
        # Get our best move. I think?
        maxQ = np.max(newQ)
        y = np.zeros((1, 3))
        y[:] = old_qval[:]
        # Check for terminal state.
        if reward_m != -500:  # non-terminal state
            update = (reward_m + (GAMMA * maxQ))
        else:  # terminal state
            update = reward_m
        # Update the value for the action we took.
        y[0][action_m] = update
        print ('y',y)
        print ('action_m',action_m)
        X_train.append(old_state_m.reshape(NUM_INPUT,))
        y_train.append(y.reshape(3,))

    X_train = np.array(X_train)
    y_train = np.array(y_train)

    return X_train, y_train


def params_to_filename(params):
    return str(params['nn'][0]) + '-' + str(params['nn'][1]) + '-' + \
            str(params['batchSize']) + '-' + str(params['buffer'])


def launch_learn(params):
    filename = params_to_filename(params)
    print(("Trying %s" % filename))
    # Make sure we haven't run this one.
    if not os.path.isfile('results/sonar-frames/loss_data-' + filename + '.csv'):
        # Create file so we don't double test when we run multiple
        # instances of the script at the same time.
        open('results/sonar-frames/loss_data-' + filename + '.csv', 'a').close()
        print("Starting test.")
        # Train.
        model = neural_net(NUM_INPUT, params['nn'])
        train_net(model, params)
    else:
        print("Already tested.")


if __name__ == "__main__":
    if TUNING:
        param_list = []
        nn_params = [[164, 150], [256, 256],
                     [512, 512], [1000, 1000]]
        batchSizes = [40, 100, 400]
        buffers = [10000, 50000]

        for nn_param in nn_params:
            for batchSize in batchSizes:
                for buffer in buffers:
                    params = {
                        "batchSize": batchSize,
                        "buffer": buffer,
                        "nn": nn_param
                    }
                    param_list.append(params)

        for param_set in param_list:
            launch_learn(param_set)

    else:
        nn_param = [164, 150]
        params = {
            "batchSize": 100,
            "buffer": 50000,
            "nn": nn_param
        }
        model = neural_net(NUM_INPUT, nn_param)
        train_net(model, params)          