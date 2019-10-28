with plt.style.context("seaborn"):
    figure, ax_list = plt.subplots(nrows=1, ncols=2, figsize=(15.36, 7.68))
    img_axes = figure.add_axes([0.0, 0.0, 0.5, 1.0])#ax_list[0]#
    plot_axes = ax_list[1]#figure.add_axes([0.5, 0.0, 1.0, 1.0])
    clock_axes = figure.add_axes([0.72, 0.94, 0.1, 0.1])
    output_file_name="swis_peaky.mp4"

    time_range = pd.date_range(start=pd.Timestamp("2019-06-25 16:00", tz=pytz.utc), end=pd.Timestamp("2019-06-28 16:00", tz=pytz.utc), freq="15T")
    metadata = dict(title="South West Interconnected System Power Station Generation",
                    artist="Owen Lamont",
                    comment="Video showing daily fluctuations in net power station generationv(excludes residential DER)")
    file_writer = FFMpegWriter(fps=12)
    with file_writer.saving(figure, output_file_name, dpi=100):
        for index, time_stamp in enumerate(time_range[1:-1]):
            if index == 0:
                continue
            img_axes.cla()
            plot_axes.cla()
            clock_axes.cla()

            # Remove axes from image plots
            img_axes.set_axis_off()
            clock_axes.set_axis_off()

            # Render the image
            image_index = image_df.index.get_loc(time_stamp, method="nearest")
            satellite_image: np.ndarray = plt.imread(image_df.iloc[image_index, 0])
            img_axes.imshow(satellite_image[3756:4524,1300:2068])

            #june_swis_pivot_df.loc[time_range[0]:time_stamp, "Total EOI (MW)"].plot(ax=plot_axes)
            plot_axes.plot("Local Time", "Total EOI (MW)", data=swis_resampled_df[time_range[0]:time_stamp])
            plot_axes.set_title("SWIS Plant Generation")
            plot_axes.set_xlabel("Time")
            plot_axes.set_ylabel("Plant Generation (MW)")
            plot_axes.set_xlim(time_range[0],time_range[-1])
            plot_axes.set_ylim(0,3500)
            plot_axes.xaxis.set_major_formatter(date_formatter)
            plt.setp(plot_axes.xaxis.get_majorticklabels(), rotation=70)
            #plot_axes.format_xdata = mdates.DateFormatter("%d %b %H:%M")

            # Render the time of day text
            clock_axes.text(
                0.0,
                0.0,
                f"""{time_stamp.tz_convert(pytz.timezone("Australia/Perth"))}""",
                fontsize=24,
                horizontalalignment="center",
                color="black",
            )

            file_writer.grab_frame()