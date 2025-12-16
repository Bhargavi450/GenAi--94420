import streamlit as st

with st.form(key="Registration_Form"):
   st.header("Registration Form")
   fname= st.text_input("First Name")
   lname=st.text_input("Last Name")
   email=st.text_input("Email")
   password=st.text_input("Password",type="password")
   Age=st.slider("Age",10,100,25,1)
   addr=st.text_area("Address")
   submit_btn = st.form_submit_button("Submit", type="primary")

if submit_btn:
    err_msg=""
    is_error=False
    if not fname:
        is_error=True
        err_msg+="First Name cannot be Empty.."
    if not lname:
        is_error=True
        err_msg+="Last Name cannot be Empty.."
    if not addr:
        is_error=True
        err_msg="Address cannot be Empty.."
        
    if is_error:
        st.error(err_msg)
    
    else:
      message = f"Successfully Registerd{fname}"
      st.success(message)
        