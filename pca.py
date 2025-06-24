import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


#sparkfun = {'data':[[4, 0, 8, 7, 6, 6, 4, 8, 7, 8, 9, 0, 7, 7, 5, 4, 3, 2],
#                    [60, 70, 78, 69, 50, 59, 37, 59, 50, 39, 47, 59, 70, 28, 49, 0, 40, 59],
#                    [456, 86, 234, 123, 123, 5, 8, 9, 0, 9, 8, 7, 6, 5, 6, 8, 8, 8],
#                    [4, 0, 8, 9, 6, 6, 4, 8, 7, 8, 9, 0, 7, 7, 5, 4, 3, 10]],
#            'target':[0, 1, 2, 0],
#            'target_names':['alu', 'carton', 'papier']}

def pca2D(sparkfun):

    fig = plt.figure()
    ax = fig.add_subplot(111)

    X_reduced = PCA(n_components=2).fit_transform(sparkfun['data']) # sous la forme [(x, y),(x, y),...]
    print(X_reduced[0])
    scatter = ax.scatter(
        X_reduced[:, 0], # Liste de toutes les coordonnées x
        X_reduced[:, 1], # Liste de toutes les coordonnées y
        c=sparkfun['target'],
        s=5,
        cmap = 'nipy_spectral'
    )

    ax.set(
        title="First two PCA dimensions",
        xlabel="x",
        ylabel="y",
    )
    ax.xaxis.set_ticklabels([])
    ax.yaxis.set_ticklabels([])

    # Add a legend
    legend1 = ax.legend(
        scatter.legend_elements()[0],
        sparkfun['target_names'],
        loc="center right",
        title="Classes"
    )
    ax.add_artist(legend1)

    plt.show()

def pca3D(sparkfun):

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    X_reduced = PCA(n_components=3).fit_transform(sparkfun['data'])
    scatter = ax.scatter(
        X_reduced[:, 0],
        X_reduced[:, 1],
        X_reduced[:, 2],
        c=sparkfun['target'],
        s=5,
        cmap = 'nipy_spectral'
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
        loc="center right",
        title="Classes",
        bbox_to_anchor=(1, 0.5)
    )
    ax.add_artist(legend1)

    plt.show()

#pca2D(sparkfun)