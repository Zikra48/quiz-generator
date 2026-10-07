

left,right=st.columns([1,2],gap='large')

with left:

    st.markdown('<div class="panel-kicker">01 / MAKE IT YOURS</div><h2>Build your challenge.</h2><p>A subject you love. Something new.<br>Where will curiosity take you?</p>',unsafe_allow_html=True)

    topic=st.text_area('Topic',placeholder='e.g., Machine Learning, Mathematics, Python, History',max_chars=200,height=80)

    difficulty=st.selectbox('Difficulty Level',DIFFICULTIES)

    count=st.slider('Number of Questions',3,10,5)

    if st.button('Generate Quiz →',type='primary',use_container_width=True):

        try:

            with st.spinner('Creating your quiz. This usually takes a few moments…'):

                st.session_state.questions=generate_quiz(topic,difficulty,count)

            st.session_state.submitted=False
            st.session_state.pop('final_answers', None)

            for i in range(MAX_QUESTIONS): st.session_state.pop(f'answer_{i}',None)

            st.session_state.notice=f'{count} questions, one new opportunity to learn. Select an answer for each.'

            st.rerun()

        except QuizError as e: st.error(str(e))

    st.caption('01  Choose your topic\n\n02  Put your knowledge to the test\n\n03  Learn from every answer')



with right:

    st.markdown('<div class="panel-kicker">02 / EXPLORE & LEARN</div><h2>Your practice space</h2>',unsafe_allow_html=True)

    st.info(st.session_state.notice)

    questions=st.session_state.questions

    if not questions:

        st.markdown('<div class="panel" style="text-align:center;padding:55px 20px"><h2>✦</h2><h3>A little curiosity goes a long way.</h3><p>Choose a topic and your challenge level.<br>Your next learning moment starts here.</p></div>',unsafe_allow_html=True)

    else:

        answered=sum(st.session_state.get(f'answer_{i}') in LETTERS for i in range(len(questions)))

        st.progress(answered/len(questions),text=f'{answered} of {len(questions)} answered')

        # Store answer letters (A/B/C/D) directly in session state.
        for i,q in enumerate(questions):
            st.markdown(f'<div class="question-card"><h3>{i+1:02} · {html.escape(q["question"])}</h3></div>',unsafe_allow_html=True)
            st.radio(
                'Choose one',
                options=list(LETTERS),
                format_func=lambda x,q=q: f'{x}.  {q["options"][x]}',
                key=f'answer_{i}',
                index=None,
                label_visibility='collapsed',
                disabled=st.session_state.submitted
            )

        submitted=st.button(
            'Submit Quiz →',
            type='primary',
            use_container_width=True,
            disabled=st.session_state.submitted,
            key='submit_quiz'
        )

        if submitted:
            missing=[str(i+1) for i in range(len(questions))
                     if st.session_state.get(f'answer_{i}') not in LETTERS]
            if missing:
                st.warning('Please answer question(s): '+', '.join(missing))
            else:
                st.session_state.final_answers=[
                    st.session_state.get(f'answer_{i}') for i in range(len(questions))
                ]
                st.session_state.submitted=True
                st.session_state.notice='Practice complete. Your score and explanations are below.'
                st.rerun()

        if st.session_state.submitted:
            answers=st.session_state.get(
                'final_answers',
                [st.session_state.get(f'answer_{i}') for i in range(len(questions))]
            )
            score=sum(a==q['correct_answer'] for q,a in zip(questions,answers)); total=len(questions); pct=100*score/total

            msg='Beautifully done.' if score==total else "You're making progress." if pct>=60 else 'Every attempt is a step forward.'

            st.markdown(f'<div class="result-hero"><span class="eyebrow">YOUR PRACTICE, COMPLETE</span><h2>Quiz Completed! — {pct:.0f}%</h2><p>{msg}</p><b>Score: {score} / {total} &nbsp; · &nbsp; ✓ {score} correct &nbsp; · &nbsp; ✕ {total-score} incorrect</b></div>',unsafe_allow_html=True)

            for i,(q,a) in enumerate(zip(questions,answers),1):

                correct=q['correct_answer']; ok=a==correct; cls='correct' if ok else 'incorrect'; label='✓ Correct' if ok else '✕ Incorrect'

                st.markdown(f'''<div class="feedback {cls}"><b>QUESTION {i:02} · {label}</b><h3>{html.escape(q['question'])}</h3><p><strong>Your answer:</strong> {a} — {html.escape(q['options'][a])}</p><p><strong>Correct answer:</strong> {correct} — {html.escape(q['options'][correct])}</p><div class="explanation"><strong>Why this is right</strong><br>{html.escape(q['explanation'])}</div></div>''',unsafe_allow_html=True)

        if st.button('Generate New Quiz',use_container_width=True):

            st.session_state.questions=[]; st.session_state.submitted=False; st.session_state.pop('final_answers', None); st.session_state.notice='A fresh start. Choose your settings, then generate a quiz.'

            for i in range(MAX_QUESTIONS): st.session_state.pop(f'answer_{i}',None)

            st.rerun()



st.markdown('<div class="studio-footer">QUIZ STUDIO &nbsp; / &nbsp; Keep your curiosity going.<br>AI-generated practice. Check important facts with trusted learning materials.</div>',unsafe_allow_html=True)
