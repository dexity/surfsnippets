#!/usr/bin/env python
#
# Copyright 2011 Alex Dementsov
#
# Scripts for drawing pie and histogram charts using matplotlib
#


from pylab import *
import colorsys
import re

INPUT_L         = "../generated/status_lang_sort.txt"
INPUT_G         = "../generated/status_genre_sort.txt"
PIE_OUTPUT_L    = "../status_lang_pie.png"
PIE_OUTPUT_G    = "../status_genre_pie.png"
HIST_OUTPUT_L   = "../status_lang_hist.png"
HIST_OUTPUT_G   = "../status_genre_hist.png"
PIE_LIMIT_L     = 11
PIE_LIMIT_G     = 20
HIST_LIMIT_L    = 20
HIST_LIMIT_G    = 30
PATTERN = "^(.*) (\d+)$"


def get_first(filename, n):
    ls      = []
    labels  = []
    nums    = []
    f = open(filename)
    for line in f.readlines():
        p   = re.compile(PATTERN)
        l   = p.findall(line)
        if not l:
            continue
        assert len(l[0]) == 2
        label   = l[0][0]
        num     = int(l[0][1])
        labels.append(label)
        nums.append(num)
    f.close()
    labels  = labels[:n]
    labels.append("Other")
    fracs   = nums[:n]
    fracs.append(sum(nums[n:]))    
    return labels, fracs


def generate_colors(n):
    "Generates list of n+1 colors: converts HSV -> RGB and presents in  html format"
    s   = 0.6   # [0, 1] saturation
    v   = 1     # [0, 1] value

    hlist  = [0.8-i*0.8/n for i in range(n+1)]  # [0, 1] hue (shifted: [0, 0.8])
    html_colors = []
    for h in hlist:
        rgb_colors  = colorsys.hsv_to_rgb(h, s, v)
        html    = "#"
        for c in rgb_colors:
            num = str(hex(int(c*255)))  # num*255 -> hex
            num = num.lstrip("0x")
            html    += num
        html_colors.append(html)

    return html_colors


def draw_pie(inpfile, outfile, limit, caption):
    # make a square figure
    figure(figsize=(8,8))
    colors  = generate_colors(limit)

    labels, fracs   = get_first(inpfile, limit)
    pie(fracs, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True)
    title(caption, bbox={'facecolor':'0.8', 'pad':10})
    savefig(outfile)    # save instead of show()


def draw_hist(inpfile, outfile, limit, caption):
    labels, fracs   = get_first(inpfile, limit)
    N = len(fracs)
    width = 1
    ind = np.arange(N)
    figure(figsize=(8,9))
    xticks(ind+width/2., labels, rotation='270', verticalalignment='top')
    bar(ind, fracs,   width, color='b')
    title(caption, bbox={'facecolor':'0.8', 'pad':10})
    subplots_adjust(bottom=0.2)
    savefig(outfile)


if __name__ == "__main__":
    draw_pie(INPUT_L, PIE_OUTPUT_L, PIE_LIMIT_L, 'Number of Stations by Language')
    draw_pie(INPUT_G, PIE_OUTPUT_G, PIE_LIMIT_G, 'Number of Stations by Genre')
    draw_hist(INPUT_L, HIST_OUTPUT_L, HIST_LIMIT_L, 'Number of Stations by Language')
    draw_hist(INPUT_G, HIST_OUTPUT_G, HIST_LIMIT_G, 'Number of Stations by Genre')

