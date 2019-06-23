import argparse

from utils.train import train
from utils.test import test


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='shoeprint recognition')
    parser.add_argument('action', help='action type (train/test)')
    parser.add_argument('--resume', action='store_true', help='恢复已有模型继续训练')

    args = parser.parse_args()

    if args.action == "train":
        train(resume=args.resume)
    elif args.action == "test":
        test()
    else:
        print("can not parse arg {}".format(args.action))
