d3.csv('data.csv', function (error,data) {
  function tabulate(data) {
		// get columns and add flag
		var columns = [];
		for(var k in data[0]) columns.push(k);
		columns.push('Flag')

		var summary_digt = "<table class='table-sm'>"
		var summary_bar = "<table class='table-sm'>"
		var metric = "<table class='table-striped table-responsive table-sm'>"

		// append the header row
		metric += '<tr>'
		for (var i in columns){
			metric += "<th class='text-center'>" + columns[i] + '</th>';
		}
		metric += '</tr>'

		// create a row for each object in the data
		var success = 0
		var warning = 0
		var danger  = 0
		for( var i = 0; i < data.length; i++) {
			metric += '<tr>';
			for(var j in data[i]){
				if (columns[j]=='Index'){
					metric += "<td class='text-right'>" + data[i][j] + '</td>';
				}else if (columns[j]=='Metric'){
					metric += "<td class='text-left'>" + data[i][j] + '</td>';
				}else{
					metric += "<td class='text-center'>" + data[i][j] + '</td>';
				}
			}

			// 'Flag' column
			tl = data[i]["Target_Low"]
			th = data[i]["Target_High"]
			bl = data[i]["Boundry_Low"]
			bh = data[i]["Boundry_High"]
			value = data[i]["Value"]
			if (value>=tl && value<=th){
				metric += "<td class='text-center text-success'>\u25a0</td>";
				success += 1
			}else if (value>=bl && value<=bh){
				metric += "<td class='text-center text-warning'>\u25a0</td>";
				warning += 1
			}else{
				metric += "<td class='text-center text-danger'>\u25a0</td>";
				danger += 1
			}
			metric += '</tr>';
		}

		metric += '</table>';

		// Summary table
		summary_digt = '<table><tr>'
		summary_digt += "<th class='text-center text-success' width=30>\u25a0 "+success+'</th>'
		summary_digt += "<th class='text-center text-warning' width=30>\u25a0 "+warning+'</th>'
		summary_digt += "<th class='text-center text-danger' width=30>\u25a0 "+danger+'</th>'
		summary_digt += '</tr></table>'

		var total = success+warning+danger
		summary_bar = '<table><tr>'
		summary_bar += "<th class='text-center text-success'>"+'\u25a0'.repeat(success*10/total)+'</th>'
		summary_bar += "<th class='text-center text-warning'>"+'\u25a0'.repeat(warning*10/total)+'</th>'
		summary_bar += "<th class='text-center text-danger'>" +'\u25a0'.repeat(danger*10/total)+'</th>'
		summary_bar += '</tr></table>'

	  return {metric: metric, summary_digt: summary_digt, summary_bar: summary_bar};
	}

	// render the table(s)
	tables = tabulate(data);
	document.getElementById('summary-table').innerHTML = tables.summary_digt;
	document.getElementById('metric-table').innerHTML = tables.metric;
	console.log(tables.summary_digt);
	console.log(tables.summary_bar);
	console.log(tables.metric);
});