import plotly as py
import plotly.figure_factory as ff
import MySQLdb
import datetime

db = MySQLdb.connect("localhost","bacula","pazzword","bacula" )

cursor = db.cursor()

cursor.execute("select Client.Name, Job.Name, StartTime, EndTime, Status.JobStatusLong, Job.Job, Job.Level, FileSet.FileSet from Job left join Status on Job.JobStatus=Status.JobStatus left join Client on Job.ClientId=Client.ClientId left join FileSet on Job.FileSetId = FileSet.FileSetId order by JobId desc limit 100")

res=cursor.fetchall()

df=[]
task_names=[]

for r in res:
	fin=""
	start=""
	if r[3] == "0000-00-00 00:00:00" or r[3] == None:
		fin = datetime.datetime.now()
	else:
		fin=r[3]

	if r[2] == "0000-00-00 00:00:00" or r[2] == None:
		start = datetime.datetime.now()
	else:
		start=r[2]


	df.append(dict(Task=r[1],Start=start,Finish=fin,Resource=r[4], text=r[1]))
	print df[len(df)-1]
        task_names.append("<b>Job:</b>" + r[5] + "<br><b>FileSet:</b>:" + r[7] + "<br><b>Status:</b> " + r[6] + "<br><b>Duration:</B>" + str(fin - start))


colors = {
'Canceled by user' : 'rgb( 255,255,2 )',
'Blocked' : 'rgb( 255,0,0 )',
'Created, not yet running' : 'rgb(122, 93, 124)',
'Verify found differences' : 'rgb(203,74,44 )',
'Terminated with errors' : 'rgb( 255,0,0 )',
'Waiting for Client' : 'rgb( 101,115,131 )',
'Waiting for media mount' : 'rgb(101,115,131)',
'Running' : 'rgb( 233,171, 23)',
'Waiting for Storage daemon' : 'rgb(101,115,131 )',
'Completed successfully' : 'rgb( 52,114,53 )',
'SD despooling attributes' : 'rgb( 21, 27, 84 )',
'Waiting for client resource' : 'rgb(101,115,131 )',
'Waiting on maximum jobs' : 'rgb(101,115,131 )',
'Non-fatal error' : 'rgb( 225,0,0 )',
'Fatal error' : 'rgb( 255,0,0 )',
'Doing batch insert file records' : 'rgb(21, 27, 84)',
'Waiting for job resource' : 'rgb(101,115,131 )',
'Waiting for new media' : 'rgb(101,115,131 )',
'Waiting on higher priority jobs' : 'rgb(101,115,131)',
'Waiting for storage resource' : 'rgb(101,115,131 )',
'Waiting on start time' : 'rgb(101,115,131)'
}

fig = ff.create_gantt(df, colors=colors, index_col='Resource', title='Daily Backups', show_colorbar=True, bar_width=0.8, showgrid_x=True, showgrid_y=True, height=900,width=1500, tasks=task_names, group_tasks=True)
fig['layout'].update(autosize=False, margin=dict(l=200))

i=0
for f in fig['data']:
	try:
		f.update(text=task_names[i], hoverinfo="text+x+y")
	except:
		pass
	i=i+1

py.offline.plot(fig, filename='bacula-gantt.html')
