import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


#sparkfun = {'data':[[4, 0, 8, 7, 6, 6, 4, 8, 7, 8, 9, 0, 7, 7, 5, 4, 3, 2],
#                    [60, 70, 78, 69, 50, 59, 37, 59, 50, 39, 47, 59, 70, 28, 49, 0, 40, 59],
#                    [456, 86, 234, 123, 123, 5, 8, 9, 0, 9, 8, 7, 6, 5, 6, 8, 8, 8],
#                    [4, 0, 8, 9, 6, 6, 4, 8, 7, 8, 9, 0, 7, 7, 5, 4, 3, 10]],
#            'target':[0, 1, 2, 0],
#            'target_names':['alu', 'carton', 'papier']}

def pca(sparkfun):

    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")

    X_reduced = PCA(n_components=2).fit_transform(sparkfun['data'])
    scatter = ax.scatter(
        X_reduced[:, 0],
        X_reduced[:, 1],
        X_reduced[:, 2],
        c=sparkfun['target'],
        s=10,
    )

    ax.set(
        title="First three PCA dimensions",
        xlabel="x",
        ylabel="y",
        zlabel="z",
    )
    ax.xaxis.set_ticklabels([])
    ax.yaxis.set_ticklabels([])
    ax.zaxis.set_ticklabels([])

    # Add a legend
    legend1 = ax.legend(
        scatter.legend_elements()[0],
        sparkfun['target_names'],
        loc="upper right",
        title="Classes",
    )
    ax.add_artist(legend1)

    plt.show()

#pca(sparkfun)