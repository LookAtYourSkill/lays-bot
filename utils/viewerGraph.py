import matplotlib.pyplot as plt
import time


def generateViewerGraph(viewerList: list, streamerName: str):
    # define x
    # multiply by 5 to get minutes
    x = [i*5 for i in range(len(viewerList))]

    # define y
    # y is the viewer count list
    y = viewerList

    # convert x to hours and minutes
    # HH:MM format
    x_hours_minutes = [f'{i//60:02d}:{i%60:02d}' for i in x]

    # get indices of hours
    hours_indices = [i for i in range(len(x_hours_minutes)) if x[i] % 60 == 0]

    # create plot
    # background color is gray
    fig, ax = plt.subplots(figsize=(19.2, 10.8), facecolor='gray')

    # plot data
    # color is red, marker is a circle, where the points are, linestyle is solid
    ax.plot(x_hours_minutes, y, color='red', marker='.', linestyle='solid')
    # fill area under the curve
    # color is blue, alpha is transparency
    ax.fill_between(x=x_hours_minutes, y1=y, y2=0, color='blue', alpha=0.5)
    # generate a grid with dotted lines
    ax.xaxis.grid(color='gray', linestyle='dotted')
    ax.yaxis.grid(color='gray', linestyle='dotted')
    # set background color to gray
    ax.set_facecolor("gray")

    # set text for x and y axis
    ax.set_xlabel('Time Elapsed (HH:MM)')
    ax.set_ylabel('Viewer Count')

    # set limits for x and y axis
    ax.set_ylim(bottom=min(y), top=max(y))
    ax.set_xlim(left=min(x_hours_minutes), right=max(x_hours_minutes))

    # set title
    ax.set_title('Twitch Viewer Count')

    # rotate x axis labels
    plt.xticks([x_hours_minutes[i] for i in hours_indices], rotation=45)


    saveTime = time.strftime("%d.%m.%Y-%H.%M", time.localtime())
    return plt.savefig(f"viewerGraph-{streamerName}.png", dpi=300, bbox_inches="tight")
