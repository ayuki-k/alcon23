import os
import PIL.Image as Image
import numpy as np
import torch
from torch.utils.data import Dataset


class KanaDataset(Dataset):
    def __init__(self, df, augmentation, datadir, onehot=True):
        super(KanaDataset, self).__init__()
        self.df = df
        self.augmentation = augmentation
        self.datadir = datadir
        self.onehot = onehot
        self.num_classes = 48

    def __getitem__(self, index):
        image = np.array(
            Image.open(os.path.join(self.datadir, self.df.loc[index, "Unicode"], self.df.loc[index, "file"])))
        label = int(self.df.loc[index, "target"])
        if self.onehot:
            target = np.zeros(self.num_classes, dtype=np.float32)
            target[label] = 1.0
            target = torch.from_numpy(target)
        else:
            target = label

        image = self.augmentation(image=image)['image']

        return image, target

    def __len__(self):
        return len(self.df)


class AlconDataset(Dataset):
    def __init__(self, df, augmentation, datadir, split=True, mode='train', onehot=True):
        super(AlconDataset, self).__init__()
        self.df = df
        self.augmentation = augmentation
        self.datadir = datadir
        self.mode = mode
        self.onehot = onehot
        self.split = split
        self.num_classes = 48

    def __getitem__(self, index):
        image = np.array(Image.open(os.path.join(self.datadir, self.df.loc[index, "file"])))
        if self.mode == 'train':
            targets = []
            for i in range(1, 4):
                label = int(self.df.loc[index, f"target{i}"])
                if self.onehot:
                    target = np.zeros(self.num_classes, dtype=np.float32)
                    target[label] = 1.0
                else:
                    target = label
                targets.append(target)
            targets = np.array(targets)
            targets = torch.from_numpy(targets)
            if self.split:
                split1 = self.df.loc[index, 'split1']
                split2 = self.df.loc[index, 'split2']
                margin = self.df.loc[index, 'margin']
                img1 = image[:split1 + margin, :, :]
                img2 = image[split1 - margin:split2 + margin, :, :]
                img3 = image[split2 - margin:, :, :]
                images = list()
                for i, img in enumerate([img1, img2, img3]):
                    images.append(self.augmentation(image=img)['image'].numpy())
                images = torch.from_numpy(np.array(images))
                return images, targets
            else:
                image = self.augmentation(image=image)['image']
                return image, targets
            
        elif self.mode == 'valid':
            targets = []
            for i in range(1, 4):
                label = int(self.df.loc[index, f"target{i}"])
                if self.onehot:
                    target = np.zeros(self.num_classes, dtype=np.float32)
                    target[label] = 1.0
                else:
                    target = label
                targets.append(target)
            targets = np.array(targets)
            targets = torch.from_numpy(targets)
            if self.split:
                split1 = self.df.loc[index, 'split1']
                split2 = self.df.loc[index, 'split2']
                margin = self.df.loc[index, 'margin']
                img1 = image[:split1 + margin, :, :]
                img2 = image[split1 - margin:split2 + margin, :, :]
                img3 = image[split2 - margin:, :, :]
                images = list()
                for i, img in enumerate([img1, img2, img3]):
                    images.append(self.augmentation(image=img)['image'].numpy())
                images = torch.from_numpy(np.array(images))
                return images, targets
            else:
                image = self.augmentation(image=image)['image']
                return image, targets

        elif self.mode == 'test':
            # test
            if self.split:
                split1 = self.df.loc[index, 'split1']
                split2 = self.df.loc[index, 'split2']
                margin = self.df.loc[index, 'margin']
                img1 = image[:split1 + margin, :, :]
                img2 = image[split1 - margin:split2 + margin, :, :]
                img3 = image[split2 - margin:, :, :]
                images = list()
                for i, img in enumerate([img1, img2, img3]):
                    images.append(self.augmentation(image=img)['image'].numpy())
                images = torch.from_numpy(np.array(images))
                return images
            else:
                image = self.augmentation(image=image)['image']
                return image

    def __len__(self):
        return len(self.df)