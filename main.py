from flet import *
import requests
from graphqlclient import GraphQLClient
import json

client = GraphQLClient("http://localhost:3000/")




def main(page:Page):

	alldata = Column()

	titletxt = TextField(label="you title")
	viewstxt = TextField(label="you views")
	useridtxt = TextField(label="you user id")
	you_id = Text()

	def deletebtn(e):
		# SET VARIABEL ID YOU DELETE
		variables = {
			"id":you_id.value
		}
		query = """
			mutation($id:ID!){
				  removePost(id:$id){
				  id
				  title
				  user_id
				  }
			}

		"""
		# NOW EXECUTE QUERY AND VARIABLE
		response = client.execute(query,variables)

		# AND HIDE DIALOG
		mydialog.open = False
		alldata.controls.clear()
		read_all_data()
		page.snack_bar = SnackBar(
			Text("succes delete",size=30),
			bgcolor="red"
			)
		page.snack_bar.open = True
		page.update()

	def editandsave(e):
		variables = {
			"id":you_id.value,
			"title":titletxt.value,
			"views":int(viewstxt.value),
			"user_id":useridtxt.value
		}
		query = """
		mutation ($id:ID!,$title:String!,$views:Int!,$user_id:ID!){
			updatePost(
				id:$id,
				title:$title,
				views:$views,
				user_id:$user_id

				){
					id
					title
					views
					user_id

				}
		}

		"""
		response = client.execute(query,variables)
		mydialog.open = False
		alldata.controls.clear()
		read_all_data()
		page.snack_bar = SnackBar(
			Text("succes edit",size=30),
			bgcolor="blue"
			)
		page.snack_bar.open = True
		page.update()




	mydialog = AlertDialog(
		title=Text("details data"),
		content=Column([
			titletxt,
			viewstxt,
			useridtxt
			]),
		actions=[
			TextButton("delete",
				style=ButtonStyle(
					color="red"
					),
				on_click=deletebtn
				),
			TextButton("edit",
				on_click=editandsave
				),
			],
		actions_alignment="spaceEvenly"
		)



	def opendialogdetails(e):

		titletxt.value = e.control.data['title']
		viewstxt.value = e.control.data['views']
		useridtxt.value = e.control.data['user_id']
		you_id.value = e.control.data['id']

		page.dialog = mydialog 
		mydialog.open = True
		page.update()

	# AND NOW CREATE READ ALL DATA FROM GRAPHQL
	def read_all_data():
		query = """
		query {
		  allPosts{
		    id
		    title
		    views
		    user_id
		  }

		}
		"""
		response = client.execute(query)
		# AND NOW CONVERT TO DICT 
		response_dict = json.loads(response)
		for post in response_dict['data']['allPosts']:
			print(post)

			# AND NOW APPEND TO WIDGET COLUM
			alldata.controls.append(
				ListTile(
					title=Text(f"id : {post['id']}"),
					subtitle=Row([
						Text(post['title']),
						Text(post['views']),
						Text(post['user_id']),

						]),
					data=post,
					on_click=opendialogdetails

					)

				)
		page.update()


	# CALL FUNCTION WHEN FLET IS FIRST RUNNIGN
	read_all_data()


	def addnewdata(e):
		title = titletxt.value
		views = int(viewstxt.value)
		user_id = useridtxt.value
		variables = {
			"title":title,
			"views":views,
			"user_id":user_id

		}

		query = """
		mutation createPost($title:String!,$views:Int!,$user_id:ID!){
			createPost(title:$title,views:$views,user_id:$user_id){
				id 
				title
				views
				user_id
			}
		}

		"""
		response = client.execute(query,variables)
		alldata.controls.clear()
		read_all_data()
		page.snack_bar = SnackBar(
			Text("succes add",size=30),
			bgcolor="green"
			)
		page.snack_bar.open = True
		page.update()



	page.add(
	AppBar(
	title=Text("flet graphql",color="white"),
	bgcolor="blue"
		),
	Column([
		titletxt,
		viewstxt,
		useridtxt,
		ElevatedButton("add now",
			bgcolor="blue",color="white",
			on_click=addnewdata
			),
		alldata
		])
		)
flet.app(target=main)
