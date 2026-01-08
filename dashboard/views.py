from __future__ import annotations
import streamlit as st
import pandas as pd
from .state import DashboardFilters

def render_data_tab(tab, df: pd.DataFrame, filtered: pd.DataFrame) -> None:
    """📑 데이터 탭 렌더링"""
    with tab:
        st.subheader("📑 데이터 탭")
        with st.expander("원본 데이터 보기(펼치기)", expanded=False):
            st.table(df)
        
        st.markdown("### 🎯 필터 결과 데이터")
        if filtered.empty:
            st.warning("선택한 조건에 해당하는 데이터가 없습니다. 사이드바 조건을 바꿔보세요.")
        else:
            st.table(filtered)

def render_chart_tab(tab, filtered: pd.DataFrame) -> None:
    """📈 차트 탭 렌더링"""
    with tab:
        st.subheader("📈 차트 탭 (차트 + Metric)")
        if filtered.empty:
            st.info("표시할 데이터가 없습니다. 사이드바에서 도시를 선택해보세요.")
            return

        # 지표 계산
        total_pop = float(filtered["인구수"].sum())
        avg_pop = float(filtered["인구수"].mean())
        max_row = filtered.sort_values("인구수", ascending=False).iloc[0]["도시"]

        st.markdown("### 📌 요약 지표 (Metric)")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("총 인구(합)", f"{total_pop:,.0f} (만 명)")
        with col2:
            st.metric("평균 인구", f"{avg_pop:,.1f} (만 명)")
        with col3:
            st.metric("최대 도시", max_row)

        st.divider()
        
        # 차트 출력
        chart_series = filtered.set_index("도시")["인구수"]
        st.markdown("### 📊 막대 차트 (도시별 인구 비교)")
        st.bar_chart(chart_series)
        st.markdown("### 📈 라인 차트 (도시별 인구를 선으로 보기)")
        st.line_chart(chart_series)
        st.caption("※ 현재는 '연도 1개'만 선택하므로 시간 추세 분석보다는 '도시 간 비교'용으로 봅니다.")

def render_monitor_tab(tab, filtered: pd.DataFrame, state: DashboardFilters) -> None:
    """🚨 관제(경고) 탭 렌더링"""
    with tab:
        st.subheader("🚨 관제(경고) 탭")
        
        if filtered.empty:
            st.info("데이터가 없습니다. 사이드바 필터(연도/도시)를 조정해보세요.")
            return

        # 1. 경고 데이터 추출 (.copy() 사용으로 독립성 확보)
        danger = filtered[filtered["인구수"] >= state.warn_threshold].copy()
        
        st.write(f"✅ 현재 경고 기준: 인구수 ≥ {state.warn_threshold} (만 명)")
        st.caption("관제 화면의 핵심은 '모든 데이터'가 아니라 '문제가 되는 것만 빠르게 추려 보여주기'입니다.")

        if danger.empty:
            st.success("✅ 현재 기준으로 경고 대상 도시가 없습니다.")
        else:
            st.error(f"⚠️ 경고 대상 도시가 {len(danger)}개 있습니다. 아래 목록을 확인하세요.")

            # 내림차순 정렬
            danger_sorted = danger.sort_values("인구수", ascending=False)

            # (1) 경고 대상 전체 목록
            st.markdown("### 📋 경고 대상 목록")
            st.table(danger)

            # (2) 🔥 우선 확인 TOP 3 (누락되었던 부분)
            st.markdown("### 🔥 우선 확인 TOP 3")
            top3 = danger_sorted.head(3)
            # 깔끔하게 도시, 연도, 인구수만 선택하여 출력
            st.table(top3[["도시", "연도", "인구수"]])

            # (3) 관제 요약 카드
            st.markdown("### 📌 관제 요약")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("경고 도시 수", f"{len(danger)}개")
            with col2:
                st.metric("최대 인구(경고 중)", f"{danger['인구수'].max():,.0f}")
            with col3:
                st.metric("평균 인구(경고 중)", f"{danger['인구수'].mean():,.1f}")