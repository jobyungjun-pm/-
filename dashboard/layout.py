from __future__ import annotations
import streamlit as st

def setup_page() -> None:
    """페이지 기본 설정 및 헤더"""
    st.title("🏙️ 대한민국 도시 인구 대시보드")
    st.write("탭으로 화면을 나눕니다.")

def create_tabs() -> tuple[st.delta_generator.DeltaGenerator, ...]:
    """3개의 메인 탭 생성"""
    return st.tabs(["📑 데이터", "📈 차트", "🚨 관제(경고)"])