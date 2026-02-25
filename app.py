import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
from modules.auth_manager import load_env, get_env_var, register_agent, update_env
from modules.api_client import SuperteamClient
from modules.ai_architect import AIArchitect
from modules.heartbeat_manager import HeartbeatManager

# --- INITIALIZATION ---
load_env()
# Initialize Heartbeat
hb = HeartbeatManager(agent_name=get_env_var("AGENT_NAME", "Alhibb-Architect"))

st.set_page_config(
    page_title="Alhibb Architect Command Center",
    page_icon="🤖",
    layout="wide"
)

# --- SESSION STATE ---
if "selected_bounty" not in st.session_state:
    st.session_state.selected_bounty = None

# --- SIDEBAR: CREDENTIALS & REGISTRATION ---
st.sidebar.title("🛠️ Agent Identity")

agent_key = get_env_var("SUPERTEAM_AGENT_KEY")
agent_name = get_env_var("AGENT_NAME")
claim_code = get_env_var("AGENT_CLAIM_CODE")

if not agent_key:
    st.sidebar.warning("No Agent Registered")
    reg_name = st.sidebar.text_input("Agent Name", placeholder="e.g. Alhibb-Architect-1")
    if st.sidebar.button("🚀 Register Agent"):
        if reg_name:
            with st.spinner("Registering..."):
                auth_data = register_agent(reg_name)
                if auth_data:
                    st.sidebar.success("Registration Successful!")
                    st.rerun()
                else:
                    st.sidebar.error("Registration Failed.")

    st.sidebar.markdown("---")
    with st.sidebar.expander("🔑 Already have an Agent Key?"):
        manual_key = st.text_input("Enter your `sk_...` key", type="password")
        manual_id = st.text_input("Agent ID (optional)")
        if st.button("🔌 Connect Existing Agent"):
            if manual_key:
                update_env("SUPERTEAM_AGENT_KEY", manual_key)
                if manual_id:
                    update_env("AGENT_ID", manual_id)
                st.success("Key connected! Reloading...")
                st.rerun()
else:
    st.sidebar.success(f"🟢 Agent Online: {agent_name}")
    st.sidebar.info(f"**Agent ID:** {get_env_var('AGENT_ID')}")
    if claim_code:
        st.sidebar.markdown(f"""
        ### 💰 Payout Claim Code
        **`{claim_code}`**
        
        [Link to Human Profile](https://superteam.fun/earn/claim/{claim_code})
        """)

# Socials / Meta
st.sidebar.markdown("---")
st.sidebar.markdown(f"🔗 [Github]({get_env_var('AGENT_GITHUB')})")
st.sidebar.markdown(f"𝕏 [Twitter]({get_env_var('AGENT_X')})")
st.sidebar.markdown(f"📱 Telegram: `{get_env_var('AGENT_TELEGRAM')}`")

# --- HEARTBEAT DISPLAY ---
st.sidebar.markdown("---")
st.sidebar.subheader("💓 Agent Heartbeat")
heartbeat_data = hb.generate_heartbeat()
st.sidebar.json(heartbeat_data)
if st.sidebar.button("📡 Broadcast Heartbeat"):
    st.sidebar.success("Heartbeat synced to console!")

# --- MAIN UI ---
st.title("🏛️ Alhibb Architect Command Center")

if not agent_key:
    st.info("👈 Please register your agent in the sidebar to start discovery.")
else:
    tab1, tab2 = st.tabs(["🔍 Bounty Discovery", "🏗️ Workspace & Submission"])
    
    client = SuperteamClient(agent_key)
    gemini_key = get_env_var("GEMINI_API_KEY")
    ai_architect = AIArchitect(gemini_key) if gemini_key else None

    # --- TAB 1: BOUNTY DISCOVERY ---
    with tab1:
        st.header("Discovered Bounties")
        if st.button("🔄 Refresh Listings"):
            with st.spinner("Fetching live listings..."):
                listings = client.get_live_listings()
                if listings:
                    # Filter for agents
                    filtered = [l for l in listings if l.get("agentAccess") in ["AGENT_ALLOWED", "AGENT_ONLY"]]
                    st.session_state.listings = filtered
                else:
                    st.error("No listings found or API error.")

        if "listings" in st.session_state and st.session_state.listings:
            for l in st.session_state.listings:
                with st.container(border=True):
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.subheader(l.get("title", "Untitled"))
                        st.markdown(f"**Reward:** {l.get('rewardAmount', 'TBD')} {l.get('token', '')}")
                        deadline_str = l.get("deadline", "No Deadline")
                        if deadline_str != "No Deadline":
                            try:
                                dt = datetime.fromisoformat(deadline_str.replace('Z', '+00:00'))
                                deadline_str = dt.strftime("%Y-%m-%d %H:%M")
                            except:
                                pass
                        st.caption(f"🗓️ **Deadline:** {deadline_str} | 🏷️ Slug: {l.get('slug')} | 🛠️ Type: {l.get('type')}")
                    with col2:
                        if st.button("🎯 SELECT", key=f"sel_{l.get('id')}"):
                            st.session_state.selected_bounty = l
                            hb.set_status("ok", last_action=f"Selected bounty: {l.get('title')}", next_action="Generating architectural solution")
                            st.success(f"Selected: {l.get('title')}")
                            st.rerun() # Optional: auto-switch to Tab 2
        else:
            st.write("Click 'Refresh Listings' to see live bounties.")

    # --- TAB 2: WORKSPACE & SUBMISSION ---
    with tab2:
        if not st.session_state.selected_bounty:
            st.write("Please select a bounty from the Discovery tab first.")
        else:
            bounty = st.session_state.selected_bounty
            slug = bounty.get("slug")
            listing_id = bounty.get("id")
            
            st.header(f"Workspace: {bounty.get('title')}")
            st.markdown(f"**Reward:** {bounty.get('rewardAmount', 'TBD')} {bounty.get('token', '')}")
            
            # Directory creation
            workspace_path = f"submissions/{slug}"
            os.makedirs(workspace_path, exist_ok=True)
            
            st.info(f"📁 Local Workspace: `{workspace_path}/`")
            
            col_in, col_ai = st.columns(2)
            
            with col_in:
                st.subheader("Submission Details")
                gist_link = st.text_input("Gist / Repo Link", placeholder="https://gist.github.com/...")
                tg_handle = st.text_input("Telegram Handle", value=get_env_var("AGENT_TELEGRAM", ""))
                other_info = st.text_area("Other Info (Description)", height=200)
                
                if st.button("🚀 Submit Entry"):
                    if not gist_link:
                        st.error("Gist link is required.")
                    else:
                        with st.spinner("Submitting to Superteam..."):
                            tg_url = f"http://t.me/{tg_handle.replace('@', '')}" if tg_handle else ""
                            hb.set_status("ok", last_action=f"Submitting to {listing_id}", next_action="Awaiting API receipt")
                            result, error_msg = client.create_submission(
                                listing_id=listing_id,
                                link=gist_link,
                                telegram=tg_url,
                                other_info=other_info
                            )
                            if result:
                                hb.set_status("ok", last_action=f"Successfully submitted to {listing_id}", next_action="Monitoring results")
                                st.balloons()
                                st.success("Submission successful!")
                                # Save receipt
                                receipt = {
                                    "timestamp": datetime.now().isoformat(),
                                    "listingId": listing_id,
                                    "slug": slug,
                                    "submission": result
                                }
                                with open(f"{workspace_path}/submission_receipt.json", "w", encoding="utf-8") as f:
                                    json.dump(receipt, f, indent=4)
                            else:
                                st.error(f"Submission failed: {error_msg}")
            
            with col_ai:
                st.subheader("🤖 AI Architect Assistant")
                if ai_architect:
                    if st.button("🧠 Generate Solution with Gemini"):
                        with st.spinner("Gemini is architecting..."):
                            hb.set_status("ok", last_action=f"Architecting solution for {bounty.get('title')}", next_action="Reviewing solution")
                            # Using title and any description available if bounty has it
                            desc = bounty.get("description", "No description provided.")
                            solution = ai_architect.generate_solution(bounty.get("title"), desc)
                            st.markdown(solution)
                            # Save to local file
                            with open(f"{workspace_path}/ai_solution.md", "w", encoding="utf-8") as f:
                                f.write(solution)
                            st.success(f"Solution saved to `{workspace_path}/ai_solution.md`")
                            
                            # NEW: Auto-generate README.md
                            readme_content = f"# {bounty.get('title')}\n\n## Overview\n{bounty.get('description', 'Solution generated by Alhibb Architect Agent.')}\n\n## Technical Implementation\n{solution}\n\n---\n*Submitted by Alhibb Architect Agent via Superteam Earn*"
                            with open(f"{workspace_path}/README.md", "w", encoding="utf-8") as f:
                                f.write(readme_content)
                            st.info("📄 Professional `README.md` also generated in workspace.")
                else:
                    st.warning("GEMINI_API_KEY missing in .env. AI features disabled.")
            
            # --- FILE PREVIEWER ---
            st.markdown("---")
            st.subheader("📁 Workspace Preview")
            files = [f for f in os.listdir(workspace_path) if os.path.isfile(os.path.join(workspace_path, f))]
            if files:
                selected_file = st.selectbox("Select file to preview", files)
                file_path = os.path.join(workspace_path, selected_file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                if selected_file.endswith(".json"):
                    st.json(content)
                elif selected_file.endswith(".md"):
                    st.markdown(content)
                else:
                    st.code(content)
                
                # NEW: Download button for cloud accessibility
                st.download_button(
                    label=f"📥 Download {selected_file}",
                    data=content,
                    file_name=selected_file,
                    mime="text/plain"
                )
            else:
                st.caption("No files in workspace yet.")
