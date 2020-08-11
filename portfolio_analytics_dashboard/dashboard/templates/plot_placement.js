// plots the figure with id
// id must match the div id above in the html
var figures = {{figuresJSON | safe}};
var ids = {{ids | safe}};
for(var i in figures) {
    Plotly.plot(ids[i],
        figures[i].data,
        figures[i].layout || {});
}