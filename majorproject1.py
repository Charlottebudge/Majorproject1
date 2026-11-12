import json
import flet as ft
import os
import shutil
import asyncio

def main(page: ft.Page):
    page.theme = ft.Theme(color_scheme_seed="#BF2E4D")
    page.title = "Twiddly's Dating Service"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    def main_page():
      page.controls.clear()
      greeting = ft.Text(value="Welcome to Twiddly's Dating Service!\nPlease login or register.",  text_align=ft.TextAlign.CENTER)
      def register(e):
        register_page(False)
      def login(e):
        login_page()
      register_button = ft.Button(content="Register", icon=ft.Icons.APP_REGISTRATION, on_click=register)
      login_button = ft.Button(content="Login", icon=ft.Icons.LOGIN, on_click=login)
      page.add(ft.Container(expand=True, content=ft.Column(controls=[greeting, ft.Row(controls=[register_button, login_button], alignment=ft.MainAxisAlignment.CENTER )], scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)))

    def login_page():
      page.controls.clear()
      greeting = ft.Text(value="Please enter your login information.")
      data = [ft.TextField(label = "Username", hint_text="Enter your username"), 
              ft.TextField(label = "Password", hint_text="Enter your password", password=True, can_reveal_password=True)]
      def save_user(e):
        global user
        accounts = {}
        try:
          #If there is saved data, checks if the inputted password matches the password saved by username in the files
          with open("accounts.json", 'r') as f:
            accounts = json.load(f)
          if accounts[data[0].value][0] == data[1].value:
            user=data[0].value
            page.add(ft.Text(value="Login successful."))
            home_page()
          else:
            page.add(ft.Text(value="Incorrect username or password, please try again."))
        except:
          page.add(ft.Text(value="No account information. Please register first."))
      submit_button = ft.Button(content="Submit", icon=ft.Icons.KEYBOARD_RETURN, on_click=save_user)
      back_button = ft.Button(content="Back", on_click=main_page, icon=ft.Icons.UNDO)
      page.add(ft.Container(expand=True, content=ft.Column(controls=[greeting, *data, ft.Row(controls=[back_button, submit_button], alignment=ft.MainAxisAlignment.CENTER)], scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)))
    
    def questionnaire_page():
      global user
      global counter
      global questions
      page.controls.clear()
      greeting = ft.Column(ft.Text(value="Thank you for registering with our service!\nPlease complete the questionnaire so we can find you your best match.", size=18, text_align=ft.TextAlign.CENTER), alignment=ft.MainAxisAlignment.CENTER)
      question_texts = [ "I consistently wait until the last minute to complete deadline activities.", 
                        "I need periods of alone time during the day to function properly.", 
                        "If I were dropped into the wilderness with nothing but a pocket knife, I would easily survive for a month.", 
                        "I hate movies with sad or tragic endings.", 
                        " I always seek a second opinion from friends or family before making an important decision.", 
                        " I would rather live in a messy room for days than clean it up regularly.", 
                        " I would rather have a friend who is brutally honest and occasionally offensive than one who is overly polite but fake.", 
                        "Shrek is a cinematic masterpiece.", 
                        "It takes me a long time to warm up to people.", 
                        "I am practically never wrong when it comes to arguments or debates.",
                        "Slow walkers deeply annoy me.", 
                        "I read the entire instruction manual when attempting to assemble a new piece of furniture.",
                        "I would rather be hated for who I truly am than loved for a fake persona.",
                        "You can instantly tell exactly what I am thinking just by looking at my facial expression.",
                        "It is the store employee’s responsibility to put my cart back in the corral.",
                        "I would allow a child to win against me in a competitive game.",
                        "I would rather work a boring, low-stress job than an entertaining, high-stress one.",
                        "I would rather sleep in a slightly uncomfortable bed or environment than speak up and potentially inconvenience my host.",
                        "I prefer a night in to a night out.",
                        "The end always justifies the means, no matter what it takes.",
                        "I enjoy playing sports or working out regularly",
                        "I would rather spend a free afternoon gaming or watching shows than being outdoors.",
                        "I am perfectly fine letting someone else make 100% of the decisions. ",
                        "I would rather do an entire group project by myself than delegate tasks and risk a mediocre grade."]
      questions = [
        ft.Column(
          controls=[
            ft.Text(text, size=18, text_align=ft.TextAlign.CENTER),
            ft.SegmentedButton(
            allow_empty_selection=True,
            allow_multiple_selection = False,
            segments=[
              ft.Segment(
                value="1",
                label="Strongly Disagree",
                icon=ft.Icons.SENTIMENT_VERY_DISSATISFIED_ROUNDED),
              ft.Segment(
                value="2",
                label="Disagree",
                icon=ft.Icons.SENTIMENT_DISSATISFIED_ROUNDED),
              ft.Segment(
                value="3",
                label="Neutral",
                icon=ft.Icons.SENTIMENT_NEUTRAL_OUTLINED),
              ft.Segment(
                value="4",
                label="Agree",
                icon=ft.Icons.SENTIMENT_SATISFIED_ROUNDED),
              ft.Segment(
                value="5",
                label="Strongly Agree",
                icon=ft.Icons.SENTIMENT_VERY_SATISFIED_ROUNDED),
              ],
            ),
          ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER) for text in question_texts]
      counter=0
      data={}
      try:
        with open ("data.json", "r") as f:
          data=json.load(f)
      except:
        pass
      if user in data:
        for x in range(len(questions)):
          questions[x].controls[1].selected=[data[user][x]]

      def submit_questionnaire(e):
        #Checks to see if the final question is answered
        if questions[counter].controls[1].selected:
          #Creates a list with the answers of each question
          new_data = [list(x.controls[1].selected)[0] for x in questions]
          #Adds/overwrites questionnaire answers
          data[user]= new_data
          with open("data.json", "w") as f:
            json.dump(data, f)
          home_page()
        else:
          show_current_question()
          page.add(ft.Text(value="Please select an answer before continuing.", color=ft.Colors.RED_ACCENT))
        
      
      def show_current_question():
        global counter
        page.controls.clear()
        back_button=ft.Button(content="Back", icon=ft.Icons.UNDO, on_click=subtracting)
        submit_button=ft.Button(content="Submit" if counter == len(questions) - 1 else "Continue", icon=ft.Icons.CHECK_CIRCLE if counter == len(questions) - 1 else ft.Icons.KEYBOARD_RETURN, on_click=submit_questionnaire if counter == len(questions) - 1 else adding)

        page.add(ft.Container(expand=True, content=ft.Column(controls=[questions[counter], ft.Row(controls=[back_button, submit_button], alignment=ft.MainAxisAlignment.CENTER), ft.ProgressBar(width=600, bar_height=18, value=(counter+1)/len(questions))], scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)),)

      def adding(e):
        global counter
        global questions
        #makes sure the user fills out the question before proceeding to the next
        if questions[counter].controls[1].selected:
            if counter < len(questions) - 1:
                counter += 1
                show_current_question()
        else:
            show_current_question()
            page.add(ft.Text(value="Please select an answer before continuing.", color=ft.Colors.RED_ACCENT))
            
      def subtracting(e):
        global counter
        #Takes user back one page, either to previous question or the start of questionnaire
        if counter > 0:
            counter -= 1
            show_current_question()
        else:
            questionnaire_page()
      
      page.add(ft.Container(expand=True, content=ft.Column(controls=[greeting, ft.Row(controls=[ft.Button(content="Start Questionnaire", icon=ft.Icons.PLAY_ARROW, on_click=show_current_question)], alignment=ft.MainAxisAlignment.CENTER)], scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)))
      if user in data:
        page.add(ft.Column(controls=[ft.Button(content="Back", on_click=home_page, icon=ft.Icons.UNDO)],  alignment=ft.MainAxisAlignment.CENTER))
                
    def register_page(edit): 
      global user
      page.controls.clear()   
      greeting = ft.Text(value="Welcome!\nPlease register your account.", text_align=ft.TextAlign.CENTER)
      userpick= ft.TextField(label = "Username", hint_text="Enter your username")
      data = [ft.TextField(label = "Password", hint_text="Enter your password", password=True, can_reveal_password=True),
              ft.TextField(label = "Confirm password", hint_text="Enter your password", password=True, can_reveal_password=True),
              ft.TextField(label = "Name", hint_text="Enter your name"),
              ft.TextField(label = "Age", hint_text="Enter your age"),]
      gender = [
          ft.Column(
              horizontal_alignment=ft.CrossAxisAlignment.CENTER,
              width=page.width,
              controls=[
                  ft.Text("What is your gender?", size=18, text_align=ft.TextAlign.CENTER),
                  ft.RadioGroup(content=ft.Row(
                    controls=[ 
                      ft.Radio(value="F", label="Female"),
                      ft.Radio(value="M", label="Male"),
                      ft.Radio(value="O", label="Other"),], 
                    alignment=ft.MainAxisAlignment.CENTER)
                    )])]
      preference = [
          ft.Column(
              horizontal_alignment=ft.CrossAxisAlignment.CENTER,
              width=page.width,
              controls=[
                  ft.Text("I am looking for a:", size=18, text_align=ft.TextAlign.CENTER),
                  ft.RadioGroup(content=ft.Row(
                    controls=[ 
                      ft.Radio(value="F", label="Girl"),
                      ft.Radio(value="M", label="Guy"),
                      ft.Radio(value="O", label="No preference"),], 
                    alignment=ft.MainAxisAlignment.CENTER))])]          
      def going_back():
        #This function can be accessed as "edit profile" for existing users or as the initial registering page for new users
        #The if statement decides where the back button leads depending on if edit is True or FAlse
        if edit==True:
          home_page()
        else:
          main_page()
      
      #Defining the profile photo 
      profile_photo=ft.CircleAvatar(foreground_image_src="", content=ft.Text("", size=25), radius=100, bgcolor="#98535a", color="#FFFFFF",)
      
      file_picker = ft.FilePicker()
      page.services.append(file_picker)

      async def open_file_dialog(e):
        #Pauses in selection until user picks a file
        files = await file_picker.pick_files(allow_multiple=False, file_type=ft.FilePickerFileType.IMAGE)
        if files:
          chosen = files[0]
          #Checking if the directory path exists
          if not os.path.exists("profile_pics"):
            os.makedirs("profile_pics")
          #Renaming and adding path
          new_path = "profile_pics/" + userpick.value + "_" + chosen.name
          shutil.copy(chosen.path, new_path)
          profile_photo.foreground_image_src = new_path
      pick_button = ft.Button(content="Upload Profile Photo", icon=ft.Icons.UPLOAD_FILE, on_click=open_file_dialog)     
        
      def account_registered(e):
        global user
        accounts: dict ={}
        #Sees if all fields have been completed
        complete = all(x.value for x in [userpick, *data, gender[0].controls[1], preference[0].controls[1]])
        try:
          with open("accounts.json", 'r') as f:
            accounts=json.load(f)
        #Changed the finally to except bc i misunderstood the function of finally. I previously thought it functioned as an
        #except safeguard that ran after the try whether it was successful or not. 
        except:
          pass
        user=userpick.value
        if complete==False:
          page.add(ft.Text("Please complete all fields."))
        elif user in accounts and edit==False:
          page.add(ft.Text("Username already taken. Please select a different username."))
        elif data[3].value.isdigit()==False:
          page.add(ft.Text("Age must be a number"))
        elif data[0].value != data[1].value:
          page.add(ft.Text("Passwords do not match"))
        else:
          #Saves data
          accounts[userpick.value] =[data[0].value, data[2].value, data[3].value, gender[0].controls[1].value, preference[0].controls[1].value, profile_photo.foreground_image_src]
          with open("accounts.json", "w") as f:
            json.dump( accounts, f)
          if edit==True:
            home_page()
          else:
            questionnaire_page()
            page.add(ft.Text(value="Register successful."))
     
      back_button = ft.Button(content="Back", on_click=going_back, icon=ft.Icons.UNDO)
      if edit==True:
        with open ("accounts.json", "r") as f:
          accounts=json.load(f)
        data[0].value=accounts[user][0]
        data[1].value=accounts[user][0]
        data[2].value=accounts[user][1]
        data[3].value=accounts[user][2]
        gender[0].controls[1].value=accounts[user][3]
        preference[0].controls[1].value=accounts[user][4]
        userpick.value=user
        profile_photo.foreground_image_src = accounts[user][5]
        profile_photo.content=f"{(accounts[user][1][0]).upper()}{(accounts[user][1][1]).upper()}"
        
        buttons= ft.Row(
                controls=[
                  back_button,
                  ft.Button(content="Submit", icon=ft.Icons.KEYBOARD_RETURN, on_click=account_registered)], alignment=ft.MainAxisAlignment.CENTER )
        page.add(ft.Container(expand=True, content=ft.Column(controls=[ft.Column(controls=[greeting, profile_photo, pick_button, *data, *gender, *preference], scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER), buttons], spacing=70, scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER), ))
      else:
        register_account = ft.Button(content="Register", icon=ft.Icons.KEYBOARD_RETURN, on_click=account_registered)
        page.add(ft.Container(expand=True, content=ft.Column(controls=[greeting, profile_photo, pick_button, userpick, *data, *gender, *preference, ft.Row(controls=[back_button, register_account], alignment=ft.MainAxisAlignment.CENTER)], scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER), ))

    def home_page():
      global user
      page.controls.clear()
      
      def devchoice():
        page.controls.clear()
        back_button = ft.Button(content="Back", on_click=home_page, icon=ft.Icons.UNDO)
        page.add(ft.Column(controls=[ft.Text(value="Your match is: "), 
                                     ft.Text(value="TWIDDLY!!!!!", size=24, weight=ft.FontWeight.W_600,  color=ft.Colors.RED),
                                     back_button], 
                                     alignment=ft.MainAxisAlignment.CENTER))
      
      def edit_profile():
        #goes to register page with edit as True
        register_page(True)
      
      def saved_matches():
        page.controls.clear()
        with open ("accounts.json", "r") as f:
          people=json.load(f)
        #checks to see if there are any saved matches
        if len(people[user])>6 and people[user][6]!=[]:
          personlist=people[user][6]
          columns=(len(personlist) + 5 - 1) // 5
          printing=[ft.Container(expand=True, content=ft.Column(controls=[ft.CircleAvatar(foreground_image_src=people[x[0]][5], content=ft.Text(f"{(people[x[0]][1][0]).upper()}{(people[x[0]][1][1]).upper()}", size=25), radius=100,  bgcolor="#98535a", color="#FFFFFF",), ft.Text(f"{people[x[0]][1]}", size=18), ft.Text(f"{x[1]}% match")], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER), ) for x in personlist]         
          #adds only 5 at a time to a row to prevent overcrowding
          for z in range(columns):
            page.add(ft.Container(expand=True, content=ft.Row(controls=[printing[z * 5 + i] for i in range(5) if z * 5 + i < len(printing)],)))
        else:
          page.add(ft.Container(expand=True, content=ft.Row(controls=[ft.Text("No saved matches.")], alignment=ft.MainAxisAlignment.CENTER)))
          
        page.add(ft.Column(controls=[ft.Button(content="Home", on_click=home_page, icon=ft.Icons.HOME)], alignment=ft.MainAxisAlignment.CENTER))
        
      greeting = ft.Text(value="Welcome. Would you like to edit your questionnaire answers or generate matches?")
      questionnaire_button = ft.Button( content="Edit Answers", icon=ft.Icons.EDIT, on_click=questionnaire_page)
      twiddly_button = ft.Button( content="Developer's Pick", on_click=devchoice)
      matches_button = ft.Button(content="Generate Matches", on_click=match_page)
      profile_edit_button = ft.Button(content="Edit Profile", on_click=edit_profile)
      saved_matches_button = ft.Button(content="View Saved Matches", on_click=saved_matches)
      log_out=ft.Row(controls=[ft.Button( content="Logout", icon=ft.Icons.LOGOUT, on_click=main_page)], alignment=ft.MainAxisAlignment.END )
      page.add(ft.Container(expand=True, content=ft.Column(controls=[greeting, ft.Row(controls=[questionnaire_button, profile_edit_button, twiddly_button, matches_button, saved_matches_button], alignment=ft.MainAxisAlignment.CENTER)],scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER), alignment=ft.Alignment.CENTER,), log_out)

    def match_page():
      global pick
      global profiles
      global user
      pick=0
      page.controls.clear()
  
      def people_weeding():
        with open("accounts.json", "r") as f:
          people=json.load(f) 
        user_dict=people[user]
        #user cannot match with themself
        del people[user] 
        for x in list(people): 
          #Loops over a copy of the keys to delete items without modifying the dictionary as it runs
          #Checking age, users age gap cannot be larger than 5yrs
          if abs(int(people[x][2]) - int(user_dict[2])) > 5:
            del people[x]
        if len(people) == 0:
          page.add(ft.Text(value="There is nobody your age on this app. Meet people in real life."))
          return {}
        #Filtering out by user preferences
        if user_dict[4] == "O":
          pass
        else:
          for x in list(people): 
            # If the user's preference does not match the person's gender
            if user_dict[4] != people[x][3]:
              del people[x] 
        #Filtering out by target preferences
        for x in list(people):
          if people[x][4] == "O":
            pass
          else:
            # If the person's preference does not match the user's gender
            if people[x][4] != user_dict[3]:
              del people[x]  
        return people
      
      def ranking_system(eligible_people):
        with open("data.json", "r") as f:
          peopleanswers=json.load(f)
        compatibility={}
        user_answers = peopleanswers[user]
        for x in eligible_people:
          #In case the person didn't do the questionnaire for some reason
          if x not in peopleanswers:
            continue
          #Score begins at 96, the perfect score. Point are removed by how different answers are
          score=96
          target_answers = peopleanswers[x]
          for y in range(len(user_answers)-2):
            score -= (abs(int(target_answers[y]) - int(user_answers[y])))
          score -=(abs(abs(int(target_answers[22]) - int(user_answers[22]))-4))
          score -=(abs(abs(int(target_answers[23]) - int(user_answers[23]))-4))
          percentage = int((score / 96) * 100)
          compatibility[x] = percentage
        return compatibility
      
      def ordering_matches(scores):
        ordered_matches=[]
        #Two separate lists for username and assigned compatibility score
        personlist=list(scores.keys())
        scoreslist=list(scores.values())
        for x in range(len(scoreslist)):
          highscore=max(scoreslist)
          #Sets a minimum requirement for matches
          if highscore<=50:
            return ordered_matches
          usersindex=scoreslist.index(highscore)
          ordered_matches.append([personlist[usersindex], scores[personlist[usersindex]]])
          #Removes them from both lists so the max function does not continue to select the same person
          del scoreslist[usersindex]
          del personlist[usersindex]
        return ordered_matches

      def displaying():
        global pick
        page.controls.clear()
        userkey=profiles[pick][0]
        with open("accounts.json", "r") as f:
          people=json.load(f) 
        #Displays photo, like and dislike button, name and compatibiltiy
        profile_photo=ft.CircleAvatar(foreground_image_src=people[userkey][5], content=ft.Text(f"{(people[userkey][1][0]).upper()}{(people[userkey][1][1]).upper()}", size=25), radius=100,  bgcolor="#98535a", color="#FFFFFF",)
        like_button=ft.Button(icon=ft.Icons.FAVORITE_ROUNDED, on_click=like)
        del_button=ft.Button(icon=ft.Icons.CLOSE_ROUNDED, on_click=delete)
        page.add(ft.Container(expand=True, content=ft.Column(controls=[profile_photo, ft.Text(f"{people[userkey][1]}", size=18), ft.Text(f"{profiles[pick][1]}% match"), ft.Row(controls=[del_button, like_button], alignment=ft.MainAxisAlignment.CENTER)], scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER), ))

      def saving_picks():
        page.controls.clear()
        with open ("accounts.json", "r") as f:
          people=json.load(f)
        #Rewrites/appends new selected person list
        if len(people[user])>6:
          people[user][6]=profiles
        else:
          people[user].append(profiles)
        with open("accounts.json", "w") as f:
          json.dump(people, f)
        page.add(ft.Column(controls=[ft.Text(value="No more matches available"), ft.Button(content="Home", on_click=home_page, icon=ft.Icons.HOME)], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER))

      #If user liked, keeps person in list                  
      def like(e):
        global pick
        if pick < len(profiles) - 1:
          pick += 1
          displaying()
        else:
          saving_picks()

      #If user disliked, deletes person from list   
      def delete(e):
        global pick
        del profiles[pick]
        if pick< len(profiles):
          displaying()
        else:
          saving_picks()
      
      profiles= ordering_matches(ranking_system(people_weeding()))

      #From flet docs, an asynchronous function with await so user must watch the loading screen before viewing matches
      async def loading():
        global profiles
        message=ft.Text("Generating matches", text_align=ft.TextAlign.CENTER)
        page.add(ft.Column(controls=[ft.ProgressBar(width=400),
                            message], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment = ft.CrossAxisAlignment.CENTER))
        for i in range(0, 151):
          await asyncio.sleep(0.05)
          if i == 50:
            message.value = "Working..."
          if i == 100: 
            message.value = "Loading..."
          if i == 150:
            message.value = "Done!"
          page.update()
        if profiles:
          page.controls.clear()
          displaying()
      if profiles:
        page.run_task(loading)
      else:
        page.add(ft.Column(controls=[ft.Text("No matches found."), ft.Button(content="Home", on_click=home_page, icon=ft.Icons.HOME)], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER))
                                                  
    main_page()
#running the main
ft.run(main)

