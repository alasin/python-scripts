import numpy as np
import argparse

def get_arguments():
    parser = argparse.ArgumentParser(description="ICNet")
    parser.add_argument("--src-weights", type=str, required=True,
                        help="Path to the source weights containing batchnorm params in npy format.")
    parser.add_argument("--target-weights", type=str, required=True,
                        help="Path to where the target weights npy file would be saved.")
    return parser.parse_args()

def main():
    args = get_arguments()
    src_dict = np.load(args.src_weights, encoding='latin1').item()
    target_dict = {}
    temp_dict = {}

    for op_name in src_dict:
        idx_bn = op_name.find('_bn')
        if idx_bn == -1:
            target_dict[op_name] = src_dict[op_name]
        else:
            for param_name, data in src_dict[op_name].iteritems():
                if param_name == 'mean':
                    mean_val = data
                if param_name == 'variance':
                    variance_val = data
                if param_name == 'scale':
                    scale_val = data
                if param_name == 'offset':
                    offset_val = data
            
            actual_op_name = op_name[0:idx_bn]
            temp_dict[actual_op_name] = [mean_val, variance_val, scale_val, offset_val]
    
    for key, value in temp_dict.iteritems():
        orig_weights = target_dict[key]['weights']
        [mean_val, variance_val, scale_val, offset_val] = value

        bias = (-1 * scale_val * mean_val)
        bias = np.divide(bias, np.sqrt(variance_val))
        bias = bias + offset_val

        new_weights = scale_val * orig_weights
        new_weights = np.divide(new_weights, np.sqrt(variance_val))

        target_dict[key]['weights'] = new_weights
        target_dict[key]['biases'] = bias

    
    # Test
    '''
    b_dict = np.load('model/icnet_cityscapes_train_30k.npy', encoding='latin1').item()
    for op_name in b_dict:
        if 'conv4_4_1x1_reduce' in op_name:
            for param_name, data in b_dict[op_name].iteritems():
                print op_name, param_name
                if param_name == 'biases':
                    print data
                if param_name == 'weights':
                    print data[0, 0, 0, :]
            for param_name, data in target_dict[op_name].iteritems():
                print op_name, param_name
                if param_name == 'biases':
                    print data
                if param_name == 'weights':
                    print data[0, 0, 0, :]
    '''

    np.save(args.target_weights, target_dict)

if __name__ == '__main__':
    main()