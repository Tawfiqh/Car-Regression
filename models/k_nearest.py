from sklearn.neighbors import KNeighborsRegressor
from .BaseModel import BaseModel
import pandas as pd


class KNearest(BaseModel):
    def __init__(self) -> None:
        self.algorithm = "ball_tree"
        self.n_neighbors = 4
        self.leaf_size = 20

    def find_hyper_paramters(self, dataset, test_dataset):
        X = dataset[0]
        y = dataset[1]

        all_results = []

        for algorithm in ["auto", "ball_tree", "kd_tree", "brute"]:
            for n_neighbors in range(2, 210, 10):
                for leaf_size in range(10, 100, 10):
                    score = self._fit_hyperparameters(
                        X, y, test_dataset, n_neighbors, algorithm, leaf_size
                    )
                    results = [algorithm, n_neighbors, leaf_size, score]

                    # print(
                    #     f"Trained model with algorithm-{algorithm}  n_neighbors-{n_neighbors}  leaf_size-{leaf_size}  and score:{score}"
                    # )
                    all_results.append(results)

        df = pd.DataFrame(
            all_results, columns=["algorithm", "n_neighbors", "leaf_size", "score"],
        )
        pd.options.display.float_format = "{:,.4f}".format
        # print("Hypertuning k-nearest - results:")
        # print(df)
        # print()

        best_result = df[df["score"] == df["score"].max()]
        print("Best model result:")
        print(best_result)

        self.algorithm = best_result["algorithm"].head(1).item()
        self.n_neighbors = best_result["n_neighbors"].head(1).item()
        self.leaf_size = best_result["leaf_size"].head(1).item()

    def fit(self, dataset, dataset_train):
        X = dataset[0]
        y = dataset[1]

        # self.find_hyper_paramters(dataset, dataset_train)

        self._fit_hyperparameters(
            X, y, None, self.n_neighbors, self.algorithm, self.leaf_size
        )

    def _fit_hyperparameters(
        self, X, y, test_dataset, n_neighbors, algorithm, leaf_size
    ):
        self.model = KNeighborsRegressor(
            n_neighbors=n_neighbors, algorithm=algorithm, leaf_size=leaf_size
        )
        self.model.fit(X, y)
        if test_dataset:
            train_score = self.model.score(*test_dataset)
            return train_score
        return None
