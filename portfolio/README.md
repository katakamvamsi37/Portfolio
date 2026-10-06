# Joel Darla — Data Engineer Portfolio

Recruiter-focused Streamlit portfolio with editable JSON content and three example Data Engineering projects.

## Run locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Edit it later

For normal updates, edit only:

```text
data/portfolio.json
```

You can change your profile, links, skills, experience, projects, certifications, and education without redesigning the UI.

## Replace an example project

Inside the `projects` array, update:

- `title`
- `subtitle`
- `description`
- `problem`
- `solution`
- `impact`
- `technologies`
- `github`
- `demo`

Copy an existing project object to add another project.

## Add your real contact links

Replace the generic GitHub and LinkedIn URLs in the `profile` section. Add your email only if you want it public.

## Add your resume

Put the PDF in `assets/`, for example:

```text
assets/Joel_Darla_Resume.pdf
```

Then set:

```json
"resume_file": "Joel_Darla_Resume.pdf"
```

The app shows a Download Resume button automatically when the file exists.

## Deploy to Streamlit Community Cloud

1. Upload this project to a GitHub repository.
2. Sign in to Streamlit Community Cloud with GitHub.
3. Choose **Create app**.
4. Select your repository.
5. Use `streamlit_app.py` as the entrypoint.
6. Deploy.

After deployment, push future updates to GitHub and the connected Streamlit app can pick them up.

## Before sharing with recruiters

- Replace the 3 example projects with your real projects.
- Add your actual GitHub and LinkedIn URLs.
- Add measurable project outcomes.
- Replace the sample certification card.
- Add your resume PDF.
- Keep only skills you can confidently explain in an interview.
