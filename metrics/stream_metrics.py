import numpy as np
from sklearn.metrics import confusion_matrix

class _StreamMetrics(object):
    def __init__(self):
        """ Overridden by subclasses """
        raise NotImplementedError()

    def update(self, gt, pred):
        """ Overridden by subclasses """
        raise NotImplementedError()

    def get_results(self):
        """ Overridden by subclasses """
        raise NotImplementedError()

    def to_str(self, metrics):
        """ Overridden by subclasses """
        raise NotImplementedError()

    def reset(self):
        """ Overridden by subclasses """
        raise NotImplementedError()      

class StreamSegMetrics(_StreamMetrics):
    """
    Stream Metrics for Semantic Segmentation Task
    """
    def __init__(self, n_classes):
        self.n_classes = n_classes
        self.confusion_matrix = np.zeros((n_classes, n_classes))

    def update(self, label_trues, label_preds):
        for lt, lp in zip(label_trues, label_preds):
            self.confusion_matrix += self._fast_hist( lt.flatten(), lp.flatten() )
    
    @staticmethod
    def to_str(results):
        string = "\n"
        for k, v in results.items():
            if k!="Class IoU":
                string += "%s: %f\n"%(k, v)
        
        #string+='Class IoU:\n'
        #for k, v in results['Class IoU'].items():
        #    string += "\tclass %d: %f\n"%(k, v)
        return string

    def _fast_hist(self, label_true, label_pred):
        mask = (label_true >= 0) & (label_true < self.n_classes)
        hist = np.bincount(
            self.n_classes * label_true[mask].astype(int) + label_pred[mask],
            minlength=self.n_classes ** 2,
        ).reshape(self.n_classes, self.n_classes)
        return hist

    def get_results(self, log_name):
        from datetime import datetime

        """Returns accuracy score evaluation result.
            "Mean Acc": mean_acc_cls,
            "Mean Precision": mean_precision,
            "Mean Recall": mean_recall,
            "Mean Fall-out": mean_fallout,
            "Mean IoU": mean_iu,
        """

        self.eval_classes = [0, 1]
        hist = self.confusion_matrix[np.ix_(self.eval_classes, self.eval_classes)]

        # 原本指標
        acc = np.diag(hist).sum() / hist.sum()
        acc_cls = np.divide(np.diag(hist), hist.sum(axis=1), out=np.zeros(hist.shape[0]), where=hist.sum(axis=1)!=0)
        mean_acc_cls = np.nanmean(acc_cls)
        iu = np.divide(np.diag(hist), (hist.sum(axis=1) + hist.sum(axis=0) - np.diag(hist)), out=np.zeros(hist.shape[0]), where=(hist.sum(axis=1) + hist.sum(axis=0) - np.diag(hist))!=0)
        mean_iu = np.nanmean(iu)
        freq = hist.sum(axis=1) / hist.sum()
        fwavacc = (freq[freq > 0] * iu[freq > 0]).sum()

        # 新增: TP, FP, FN, TN
        TP = np.diag(hist).astype(np.float64)
        FP = hist.sum(axis=0) - TP
        FN = hist.sum(axis=1) - TP
        TN = hist.sum() - (TP + FP + FN)

        # 新增指標 per class
        precision = np.divide(TP, TP + FP, out=np.zeros_like(TP), where=(TP+FP)!=0)
        recall = np.divide(TP, TP + FN, out=np.zeros_like(TP), where=(TP+FN)!=0)
        fallout = np.divide(FP, FP + TN, out=np.zeros_like(FP), where=(FP+TN)!=0)

        # 平均
        mean_precision = np.nanmean(precision)
        mean_recall = np.nanmean(recall)
        mean_fallout = np.nanmean(fallout)

        print("Confusion Matrix:\n", hist)

        metrics = {
            # "Overall Acc": acc,
            # "FreqW Acc": fwavacc,
            "Mean Acc": mean_acc_cls,
            "Mean Precision": mean_precision,
            "Mean Recall": mean_recall,
            "Mean Fall-out": mean_fallout,
            "Mean IoU": mean_iu,
        }
        # 取得時間
        now = datetime.now()
        time_str = now.strftime("%Y-%m-%d %H:%M:%S")
        safe_time_str = time_str.replace(":", "_")  # 替換掉冒號

        # 寫入 log
        with open(log_name, "a") as f:
            f.write(f"{safe_time_str}\n")
            for key, value in metrics.items():
                f.write(f"{key}: {value:.4f}\n")
            f.write("matrix:\n")
            f.write(np.array2string(hist, separator=', '))
            f.write("\n\n")

        print(f"Log saved to {log_name}")

        return metrics

        
    def reset(self):
        self.confusion_matrix = np.zeros((self.n_classes, self.n_classes))

class AverageMeter(object):
    """Computes average values"""
    def __init__(self):
        self.book = dict()

    def reset_all(self):
        self.book.clear()
    
    def reset(self, id):
        item = self.book.get(id, None)
        if item is not None:
            item[0] = 0
            item[1] = 0

    def update(self, id, val):
        record = self.book.get(id, None)
        if record is None:
            self.book[id] = [val, 1]
        else:
            record[0]+=val
            record[1]+=1

    def get_results(self, id):
        record = self.book.get(id, None)
        assert record is not None
        return record[0] / record[1]
