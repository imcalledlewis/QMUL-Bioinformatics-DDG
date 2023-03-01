def LD_plot(LD, labels, title):

    n = LD.shape[0]

    figure = plt.figure()

    # mask triangle matrix
    mask = np.tri(n, k=0)
    LD_masked = np.ma.array(LD, mask=mask)

    # create rotation/scaling matrix
    t = np.array([[1, 0.5], [-1, 0.5]])
    # create coordinate matrix and transform it
    coordinate_matrix = np.dot(np.array([(i[1], i[0])
                                         for i in itertools.product(range(n, -1, -1), range(0, n + 1, 1))]), t)
    # plot
    ax = figure.add_subplot(1, 1, 1)
    ax.spines['bottom'].set_position('center')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.get_yaxis().set_visible(False)
    plt.tick_params(axis='x', which='both', top=False)
    plt.pcolor(coordinate_matrix[:, 1].reshape(n + 1, n + 1),
                   coordinate_matrix[:, 0].reshape(n + 1, n + 1), np.flipud(LD_masked), edgecolors = "white", linewidth = 1.5, cmap = 'OrRd')
    plt.xticks(ticks=np.arange(len(labels)) + 0.5, labels=labels, rotation='vertical', fontsize=8)
    plt.colorbar()

    # add title
    plt.title(f"{title}", loc = "center")
   
    return figure

LD_heatmap_plot = ld_plot(LD_matrix_df, SNP_list, "LD plot title")