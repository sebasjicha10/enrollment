<h1>Enrollment page</h1>
<h2>Description</h2>
This project consists of a simple enrollment page for courses given by my local university (UCR). <a href="#">Watch a video demo here</a>
<h2>Back End</h2>
<ul>
  <li>Python - Flask</li>
  <li>SQLite</li>
</ul>
<h2>Front End</h2>
<ul>
  <li>HTML</li>
  <li>CSS - BootStrap</li>
  <li>JavaScript</li>
</ul>
<h2>How it works</h2>
<h3>Database</h3> 
To get in, the user can log in, if previously registered, or sign up. </br>
The initial registration works with a predefined database where the university has a list of students and their corresponding students' ids,so it validates that the user is, in fact, a student at UCR.</br>
Tables are used to display and update available courses info, show a history of registrations, and update, create and display information about the students.
<h3>Sessions and Routing</h3> 
The webpage uses sessions to confirm the user is registered, and keep him or her login.</br>
Once in, a dashboard (Index page) displays a list of the already successfully enrolled courses by the user.</br>
One can add courses either by clicking on "Add Course" in the dashboard, or "Enrollment" on the navigation bar.</br>
This will redirect the user to a page where the available course options are displayed, with additional useful information.</br>
After selecting the course and providing the password, the course is added to the dashboard.</br>
Additionally, the page offers 2 more actions:</br>
"Schedule", where the enrolled courses are displayed dynamically in a weekly-hourly schedule, for visual aid,</br>
and "Personal Info" where the user can update the information given at signing up or change his or her password.</br>
