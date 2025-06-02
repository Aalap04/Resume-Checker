import os
from dotenv import load_dotenv
from Backend.core import process_resume
import streamlit as st
import tempfile
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

load_dotenv()

def get_github_token():
    """Get GitHub token from environment or Streamlit secrets"""
    # Try environment variable first (for local development)
    token = os.getenv('GITHUB_TOKEN')
    
    # If not found, try Streamlit secrets (for cloud deployment)
    if not token:
        try:
            token = st.secrets['GITHUB_TOKEN']
        except:
            pass
    
    return token

github_token = get_github_token()

st.write("🔧 Debug Info:")
if github_token:
    st.write("✅ GitHub token found")
    st.write(f"🔑 Token length: {len(github_token)} characters")
else:
    st.write("❌ No GitHub token found")
    st.write("Please check your Streamlit secrets configuration")

def fetch_github_contributions(username, token=None):
    """Fetch GitHub contribution data for heatmap"""
    try:
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Resume-Checker-App'
        }
        if token:
            headers['Authorization'] = f'token {token}'
        
        # Get user events (public activity)
        url = f"https://api.github.com/users/{username}/events"
        st.write(f"🔍 Fetching data from: {url}")
        
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            events = response.json()
            st.write("✅ Successfully fetched GitHub data")
            st.write(f"📈 Found {len(events)} events") 
            return process_events_for_heatmap(events)
        elif response.status_code == 404:
            st.warning(f"⚠️ GitHub user '{username}' not found")
            return None
        else:    
            st.write("❌ Failed to fetch GitHub data")
            return None
        
    except requests.exceptions.Timeout:
        st.error("⏰ GitHub API request timed out")
        return None
    except Exception as e:
        st.error(f"❌ Error fetching GitHub data: {str(e)}")
        return None

def process_events_for_heatmap(events):
    """Process GitHub events into heatmap data"""
    if not events:
        st.info("ℹ️ No GitHub events found")
        return {}
    
    activity_data = {}
    
    for event in events[:100]:
        created_at = event.get('created_at', '')
        if created_at:
            try:
                date = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ').date()
                date_str = date.strftime('%d/%m/%Y')
                
                if date_str in activity_data:
                    activity_data[date_str] += 1
                else:
                    activity_data[date_str] = 1
            except ValueError as e:
                st.warning(f"⚠️ Could not parse date: {created_at}")
                continue
    
    st.write(f"📊 Processed {len(activity_data)} unique activity dates") 
    return activity_data

def create_github_heatmap(activity_data, username):
    """Create a GitHub-style contribution heatmap"""
    if not activity_data or len(activity_data) == 0:
        st.warning("⚠️ No activity data available for heatmap")
        return None
    
    try:
        # Create date range for last 365 days
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=365)
        
        # Create complete date range
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Prepare data for heatmap
        heatmap_data = []
        for date in date_range:
            date_str = date.strftime('%d/%m/%Y')
            count = activity_data.get(date_str, 0)
            
            heatmap_data.append({
                'date': date,
                'day': date.strftime('%A'),
                'week': date.isocalendar()[1],
                'month': date.strftime('%B'),
                'month_year': date.strftime('%B %Y'),  # ✅ Added: Month with year
                'day_of_month': date.day,
                'count': count
            })
        
        df = pd.DataFrame(heatmap_data)
        
        # Create the heatmap using month_year for proper chronological order
        fig = go.Figure(data=go.Heatmap(
            x=df['month_year'],  # ✅ Changed: Use month with year for proper ordering
            y=df['day_of_month'],
            z=df['count'],
            colorscale=[
                [0, '#ebedf0'],      # Light gray for no activity
                [0.25, '#9be9a8'],   # Light green
                [0.5, '#40c463'],    # Medium green
                [0.75, '#30a14e'],   # Dark green
                [1, '#216e39']       # Darkest green
            ],
            hoverongaps=False,
            hovertemplate='<b>%{customdata}</b><br>Contributions: %{z}<extra></extra>',
            customdata=df['date'].dt.strftime('%d/%m/%Y'),
        ))
        
        # ✅ Fixed: Get unique months in chronological order from the data
        unique_months = df.sort_values('date')['month_year'].unique()
        
        fig.update_layout(
            title=f'GitHub Activity Heatmap - @{username}',
            xaxis_title='Month',
            yaxis_title='Day of Month',
            height=600,
            margin=dict(l=0, r=0, t=40, b=0),
            xaxis=dict(
                categoryorder='array',
                categoryarray=list(unique_months),  # ✅ Use actual chronological order
                tickangle=45  # Rotate month names for better readability
            ),
            yaxis=dict(
                tickmode='array',
                tickvals=list(range(1, 32)),
                ticktext=[str(i) for i in range(1, 32)]
            )
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating heatmap: {e}")
        return None

def create_simple_github_stats(username):
    """Fallback GitHub stats visualization"""
    try:
        st.markdown("#### 📈 GitHub Activity (Fallback)")
        
        # Try different GitHub stat services
        services = [
            f"https://ghchart.rshah.org/{username}",
            f"https://github-readme-streak-stats.herokuapp.com/?user={username}&theme=default"
        ]
        
        for service_url in services:
            try:
                st.image(service_url, caption=f"GitHub activity for @{username}")
                return True
            except:
                continue
                
        return False
        
    except Exception as e:
        st.error(f"Could not load GitHub stats: {e}")
        return False

# Page configuration
st.set_page_config(
    page_title="Resume Checker - AI-Powered Resume Analysis", 
    layout="centered",
    page_icon="📄",
    initial_sidebar_state="collapsed"
)

col1, col2, col3 = st.columns([1, 2, 1])

# Header
with col2:
    st.title("Resume Checker") 
    
st.subheader("**Is your Resume Good Enough?**")
st.markdown("*A free and fast AI resume checker doing crucial checks to ensure your resume is ready to perform and get you interview callbacks.*")

# File upload section
col1, col2 = st.columns(2)

with col1:
    st.markdown("##### 📋 Job Description")
    job_file = st.file_uploader(
        "Upload Job Description (PDF)", 
        type=["pdf"],
        help="Upload the job posting or requirements document"
    )

with col2:
    st.markdown("##### 📄 Resume")
    resume_file = st.file_uploader(
        "Upload Resume (PDF)", 
        type=["pdf"],
        help="Upload your resume in PDF format"
    )

# Validation and processing
if st.button("🚀 Analyze Resume", type="primary", use_container_width=True):
    if not job_file or not resume_file:
        st.error("⚠️ Please upload both Job Description and Resume files.")
    else:
        try:
            with st.spinner("🔍 Analyzing documents..."):
                # Create temporary files
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_job:
                    temp_job.write(job_file.read())
                    job_path = temp_job.name
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_resume:
                    temp_resume.write(resume_file.read())
                    resume_path = temp_resume.name

                # Process files
                result = process_resume(resume_path, job_path)

                # Clean up temporary files
                os.unlink(job_path)
                os.unlink(resume_path)
            
            # Display results
            st.success("✅ Analysis complete!")
            
            # Score section
            st.markdown("### 📊 Compatibility Score")
            score = result["match_score"]
            
            # Color-coded progress bar
            if score >= 80:
                color = "green"
                emoji = "🟢"
            elif score >= 60:
                color = "orange" 
                emoji = "🟡"
            else:
                color = "red"
                emoji = "🔴"
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.progress(score / 100)
            with col2:
                st.markdown(f"### {emoji} {score}%")
            
            # Skills comparison
            st.markdown("### 🎯 Skills Analysis")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Job Requirements:**")
                job_skills = result.get("job_skills", [])
                if job_skills:
                    st.write(", ".join(job_skills))
                else:
                    st.write("No specific skills extracted")
            
            with col2:
                st.markdown("**Your Skills:**")
                resume_skills = result.get("resume_skills", [])
                if resume_skills:
                    st.write(", ".join(resume_skills))
                else:
                    st.write("No specific skills extracted")

            # GitHub analysis with heatmap
            st.markdown("### 🐙 GitHub Profile Analysis")
            github_profile = result.get("github_profile")
            
            if github_profile:
                st.markdown(f"**Profile:** [View GitHub Profile]({github_profile})")
                
                gh_data = result.get("github_analysis", {})
                if "error" in gh_data:
                    st.warning("⚠️ Couldn't fetch GitHub activity data.")
                else:
                    st.metric("Public Events", gh_data.get("public_events", 0))
                
                # Add GitHub Heatmap
                username = github_profile.split('/')[-1] if github_profile.endswith('/') else github_profile.split('/')[-1]
                st.write(f"🔍 Extracted username: {username}")
                
                github_token = os.getenv('GITHUB_TOKEN')
                
                with st.spinner("Loading GitHub activity heatmap..."):
                    activity_data = fetch_github_contributions(username, github_token)
                    
                    if activity_data and len(activity_data) > 0:
                        heatmap_fig = create_github_heatmap(activity_data, username)
                        if heatmap_fig:
                            st.plotly_chart(heatmap_fig, use_container_width=True)
                        else:
                            st.info("📊 Could not create heatmap visualization")
                            create_simple_github_stats(username)
                    else:
                        st.info("📊 No recent GitHub activity found for heatmap")
                        if not create_simple_github_stats(username):
                            st.info("GitHub profile exists but no stats could be loaded")
                        
            else:
                st.info("ℹ️ No GitHub profile found in resume")

            # Recommendations section
            if hasattr(result, 'recommendations') and result.get('recommendations'):
                st.markdown("### 💡 Recommendations")
                for rec in result['recommendations']:
                    st.write(f"• {rec}")

        except Exception as e:
            st.error(f"❌ An error occurred while processing: {str(e)}")
            st.write("Please check your files and try again.")

# Information section
with st.expander("ℹ️ How it works"):
    st.markdown("""
    1. **Upload Documents**: Provide both job description and resume in PDF format
    2. **AI Analysis**: Our system extracts and compares skills, experience, and requirements
    3. **Compatibility Score**: Get a percentage match based on semantic similarity
    4. **Skills Breakdown**: See which skills match and which are missing
    5. **GitHub Integration**: Automatic detection and analysis of GitHub profiles with activity heatmap
    """)

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit • Powered by AI")