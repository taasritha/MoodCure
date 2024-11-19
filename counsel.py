import streamlit as st

def counsel_page():
    st.title("Meet Our Counselors")
    st.write("We have a team of experienced counselors here to support you on your mental health journey. Reach out to any of them for guidance and help.")

    counselors = [
        {
            "name": "Dr. Rita Bhattacharjee",
            "cabin": "SMV G12",
            "contact": "7008214473",
            "email": "rina.rani@vit.ac.in"
        },
        {
            "name": "Mr. Felix Emmanuel",
            "cabin": "TT 720",
            "contact": "9442823000",
            "email": "felix.emmanuel@vit.ac.in"
        },
        {
            "name": "Ms. Laksmi",
            "cabin": "Ladies hostel",
            "contact":"9495974552",
            "email": "lakshmi.a@vit.ac.in"
        }
    ]

    for counselor in counselors:
        st.markdown("---") 
        st.subheader(counselor["name"])
        st.write(f"**Cabin Number:** {counselor['cabin']}")
        st.write(f"📧 **Email:** [{counselor['email']}](mailto:{counselor['email']})")

        st.markdown("<br>", unsafe_allow_html=True)
