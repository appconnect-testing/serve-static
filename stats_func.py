def generate_certainity_plot(percent_value):
    import matplotlib.pyplot as plt
    from matplotlib import cm
    from math import log10

    labels = list("ABCDEFG")
    data = [percent_value-0.001, 0, 0, 0]
    n = len(data)
    k = 0.5
    m = k * (1 + (max(data)) // k)

    #radius of donut chart
    r = 1.5
    #calculate width of each ring
    w = r / n 

    #create colors along a chosen colormap
    colors = [cm.terrain(i / n) for i in range(n)]

    #create figure, axis
    fig, ax = plt.subplots()
    ax.axis("equal")

    #create rings of donut chart
    for i in range(n):
        #hide labels in segments with textprops: alpha = 0 - transparent, alpha = 1 - visible
        innerring, _ = ax.pie([m - data[i], data[i]], radius = r - i * w, startangle = 90, labels = ["", labels[i]], labeldistance = 1 - 1 / (1.5 * (n - i)), textprops = {"alpha": 0}, colors = ["white", colors[i]])
        plt.setp(innerring, width = w, edgecolor = "white")

    # Build a rectangle in axes coords
    left, width = .25, .5
    bottom, height = .25, .5
    right = left + width
    top = bottom + height
    ax.text(0.5 * (left + right), 0.5 * (bottom + top), f"{int(data[0]*100)}%",
            horizontalalignment='center',
            verticalalignment='center',
            transform=ax.transAxes, fontsize=30)

    ax.text(0.5 * (left + right), 0.4 * (bottom + top), "confidence level",
            horizontalalignment='center',
            verticalalignment='center',
            transform=ax.transAxes, fontsize=20)
    return fig
    


def generate_text(input_text):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    # Build a rectangle in axes coords
    left, width = .25, .5
    bottom, height = .25, .5
    right = left + width
    top = bottom + height
    ax.text(0.5 * (left + right), 0.5 * (bottom + top), input_text,
            horizontalalignment='center',
            verticalalignment='center',
            transform=ax.transAxes, fontsize=50)
    ax.set_axis_off()
    return fig

