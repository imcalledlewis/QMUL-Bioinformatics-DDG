# Separate by chromosome ID, and colour them
index_cmap = linear_cmap('chr_id', palette = ['grey','black']*11,low=1,high=22)

## Format figure
p = figure(frame_width=800,		# graph size
            plot_height=500, 	# graph size
            title=f"SNPs in {SNP_req} for T1D",# Title added in html
            toolbar_location="right",
            tools="""pan,hover,xwheel_zoom,zoom_out,box_zoom,
            reset,box_select,tap,undo,save""",# Tool features added to make graph interactive
            tooltips="""
            <div class="manPlot-tooltip">
                <span class=tooltip-rsid>@rsid </span>
                <span class=tooltip-chrPos>@chr_id:@chr_pos</span>
            </div>				
            """# Shows when mouse is hovered over plot
            )

# Add circles to the figure to represent the SNPs in the GWAS data
p.circle(x='cumulative_pos', y='-logp',# x and y-axis
        source=df,
        fill_alpha=0.8,# Transparency of plot
        fill_color=index_cmap,# Colour of plot
        size=7,# Size of plot 
        selection_color="rebeccapurple", # Colour of plot when selected
        hover_color="green"
        )