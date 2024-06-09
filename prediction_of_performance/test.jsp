<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
    pageEncoding="ISO-8859-1"%>
<%@ page import="model.User"%>
<%@ page import="model.Tuple"%>
<%@ page import="db.DbConnector" %>
<%@ page import="java.util.List" %>
<%@ page import="java.util.ArrayList" %>
    
<!DOCTYPE html>
<html>
<head>
<meta charset="ISO-8859-1">
<title>Change Task Status</title>
<link rel="stylesheet" type="text/css" href="CSS/WebApp.css" >	
</head>
<body>
	<%
	final User sessionUser = (User) session.getAttribute("user");
	if (sessionUser == null || request.getParameter("task_id") == null) {
		// Redirect User to Login Page
		response.sendRedirect( "Login.html"); 
	}
	String taskidn = request.getParameter("task_id");
	%>
	<%
	final List<Tuple> statusList;
	final DbConnector db = DbConnector.getInstance();
	db.openDbConnection();
	statusList= db.getStatus();
	%>
	<form action="ChangeStatus" method="POST">
		<input type="hidden" name="userid" value="<%=sessionUser.getId()%>">
		<input type="hidden" name="taskid" value="<%=request.getParameter("taskid")%>">
        <label for="status">Select New Status:</label>
	    <select name="status" id="status">
	    <%
            for (Tuple status : statusList) {
            	final String taskid = status.getFirst();
            	final String statusname = status.getSecond();
            	if (taskidn.equals(task_id)) {
            		%> <option value="<%task_id%>" selected><%=statusname%></option>
            		<%
            	}
             else {%>
            <option value="<%=taskid%>"><%=statusname%></option>
            <%
             }%>
        </select>
		  <br><br>
        <input type="hidden" name="task_id" value="<%= request.getParameter("task_id") %>">
		<input type="submit" value="Update">
	</form>

</body>
</html>