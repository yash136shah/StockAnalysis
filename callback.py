import streamlit as st









if 'count' not in st.session_state:
    st.session_state.count = 1
    st.session_state.count2 = 21
    st.session_state.il = False
    st.session_state.dl = False

def increment_counter():
    n_co =110
    n_co_ms = n_co//20 * 20

    if st.session_state.count2 == n_co_ms or st.session_state.count2 > n_co_ms:
        x=n_co - 20
        st.session_state.count = x
        st.session_state.count2 = n_co

    else:
        st.session_state.count += 20
        st.session_state.count2 += 20

    st.session_state.il = True
    st.session_state.dl = False

def decrement_counter():
    if st.session_state.count2==1 or st.session_state.count2<1:
            st.session_state.count = 1
            st.session_state.count2 = 20
    
    elif st.session_state.count2>41:
              st.session_state.count -= 20
              st.session_state.count2 -=20
             
    else:
        st.session_state.count = 1
        st.session_state.count2 = 20
    
    st.session_state.il = False
    st.session_state.dl = True

    
             


n_co =110
n_co_mm = n_co//20


next_20 = st.button("Next 20",key="companynext",on_click=increment_counter)
previous_20 = st.button("Previous 20",key="companyprev",on_click=decrement_counter)

container = st.container()

if next_20:
    ncos,ncoe =container.slider("Number of Companies to select:",1,n_co,(st.session_state.count,st.session_state.count2),on_change=increment_counter)
   
elif previous_20:
    ncos,ncoe =container.slider("Number of Companies to select:",1,n_co,(st.session_state.count,st.session_state.count2),on_change=decrement_counter)

else:
    if st.session_state.count == 1 or st.session_state.count < 1 :

        ncos,ncoe =container.slider("Number of Companies to select:",1,n_co,(1,20))
        
    else:
        if st.session_state.il == True:

          ncos,ncoe =container.slider("Number of Companies to select:",1,n_co,(st.session_state.count - 20,st.session_state.count2 -20))

        elif st.session_state.dl == True:
            ncos,ncoe =container.slider("Number of Companies to select:",1,n_co,(st.session_state.count + 20,st.session_state.count2 + 20))