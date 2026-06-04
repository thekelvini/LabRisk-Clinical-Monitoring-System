import pyodbc
import pandas as pd
from dash import Dash, html, dcc, dash_table
import plotly.express as px
import plotly.graph_objects as go


SERVER = "DESKTOP-9IJ6R5C"
DATABASE = "HospitalLabDB"

connection_string = f"""
DRIVER={{ODBC Driver 17 for SQL Server}};
SERVER={SERVER};
DATABASE={DATABASE};
Trusted_Connection=yes;
"""


def load_dashboard_data():
    query = """
        SELECT
            lr.result_id,
            lr.lab_value,
            lr.result_status,
            lr.risk_level,
            lr.result_date,
            e.encounter_id,
            p.patient_id,
            p.age,
            p.sex,
            d.diagnosis_name,
            dept.department_name,
            pr.provider_name,
            lt.lab_test_name,
            lt.unit,
            lt.reference_low,
            lt.reference_high
        FROM lab_results lr
        LEFT JOIN encounters e
            ON lr.encounter_id = e.encounter_id
        LEFT JOIN patients p
            ON e.patient_id = p.patient_id
        LEFT JOIN diagnoses d
            ON e.diagnosis_code = d.diagnosis_code
        LEFT JOIN departments dept
            ON e.department_id = dept.department_id
        LEFT JOIN providers pr
            ON e.provider_id = pr.provider_id
        LEFT JOIN lab_tests lt
            ON lr.lab_test_id = lt.lab_test_id;
    """

    connection = pyodbc.connect(connection_string)
    df = pd.read_sql(query, connection)
    connection.close()

    df["result_date"] = pd.to_datetime(df["result_date"])

    return df


df = load_dashboard_data()


total_lab_results = len(df)
total_patients = df["patient_id"].nunique()
abnormal_results = len(df[df["result_status"] != "Normal"])
critical_results = len(df[df["risk_level"] == "Critical"])
high_risk_results = len(df[df["risk_level"] == "High Risk"])
departments_monitored = df["department_name"].nunique()

abnormal_percent = (abnormal_results / total_lab_results) * 100 if total_lab_results else 0


risk_counts = (
    df.groupby("risk_level")
    .size()
    .reset_index(name="count")
)

risk_color_map = {
    "Critical": "#D9534F",
    "High Risk": "#F0AD4E",
    "Routine": "#5CB85C"
}

critical_by_department = (
    df[df["risk_level"] == "Critical"]
    .groupby("department_name")
    .size()
    .reset_index(name="critical_count")
    .sort_values("critical_count", ascending=True)
)

lab_by_department = (
    df.groupby("department_name")
    .size()
    .reset_index(name="lab_result_count")
    .sort_values("lab_result_count", ascending=True)
)

diagnosis_distribution = (
    df.groupby("diagnosis_name")
    .size()
    .reset_index(name="count")
    .sort_values("count", ascending=False)
)

trend_data = (
    df.groupby(["result_date", "risk_level"])
    .size()
    .reset_index(name="count")
)

dept_risk = (
    df.groupby(["department_name", "risk_level"])
    .size()
    .reset_index(name="count")
)

dept_risk_pivot = (
    dept_risk
    .pivot(index="department_name", columns="risk_level", values="count")
    .fillna(0)
    .reset_index()
)

for col in ["Critical", "High Risk", "Routine"]:
    if col not in dept_risk_pivot.columns:
        dept_risk_pivot[col] = 0

dept_risk_pivot["Total"] = (
    dept_risk_pivot["Critical"] +
    dept_risk_pivot["High Risk"] +
    dept_risk_pivot["Routine"]
)

age_bins = [18, 30, 45, 60, 75, 100]
age_labels = ["18-30", "31-45", "46-60", "61-75", "76+"]

df["age_group"] = pd.cut(
    df["age"],
    bins=age_bins,
    labels=age_labels,
    include_lowest=True
)

age_distribution = (
    df.drop_duplicates("patient_id")
    .groupby("age_group", observed=False)
    .size()
    .reset_index(name="patient_count")
)

gender_distribution = (
    df.drop_duplicates("patient_id")
    .groupby("sex")
    .size()
    .reset_index(name="patient_count")
)

high_risk_table = df[
    df["risk_level"].isin(["Critical", "High Risk"])
][
    [
        "patient_id",
        "age",
        "sex",
        "diagnosis_name",
        "lab_test_name",
        "lab_value",
        "unit",
        "reference_low",
        "reference_high",
        "result_status",
        "risk_level",
        "department_name",
        "provider_name",
        "result_date"
    ]
].copy()

high_risk_table["result_date"] = high_risk_table["result_date"].dt.strftime("%m/%d/%Y")

high_risk_table = high_risk_table.head(25)


def style_figure(fig):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(
            family="Segoe UI, Arial",
            size=12,
            color="#263238"
        ),
        title=dict(
            font=dict(size=16, color="#0B1F3A"),
            x=0.02
        ),
        margin=dict(l=30, r=20, t=55, b=35),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return fig


risk_fig = px.pie(
    risk_counts,
    names="risk_level",
    values="count",
    hole=0.55,
    title="Risk Level Distribution",
    color="risk_level",
    color_discrete_map=risk_color_map
)
risk_fig.update_traces(
    textposition="outside",
    textinfo="label+percent+value"
)
risk_fig = style_figure(risk_fig)


trend_fig = px.line(
    trend_data,
    x="result_date",
    y="count",
    color="risk_level",
    title="Lab Results Trend by Risk Level",
    color_discrete_map=risk_color_map,
    markers=True
)
trend_fig = style_figure(trend_fig)


lab_dept_fig = px.bar(
    lab_by_department,
    x="lab_result_count",
    y="department_name",
    orientation="h",
    title="Lab Results by Department",
    color_discrete_sequence=["#1F77B4"]
)
lab_dept_fig.update_layout(showlegend=False)
lab_dept_fig = style_figure(lab_dept_fig)


critical_dept_fig = px.bar(
    critical_by_department,
    x="critical_count",
    y="department_name",
    orientation="h",
    title="Critical Results by Department",
    color_discrete_sequence=["#D9534F"]
)
critical_dept_fig.update_layout(showlegend=False)
critical_dept_fig = style_figure(critical_dept_fig)


diagnosis_fig = px.treemap(
    diagnosis_distribution,
    path=["diagnosis_name"],
    values="count",
    title="Diagnosis Distribution",
    color="count",
    color_continuous_scale="Blues"
)
diagnosis_fig = style_figure(diagnosis_fig)


age_fig = px.bar(
    age_distribution,
    x="age_group",
    y="patient_count",
    title="Age Distribution",
    color_discrete_sequence=["#1F77B4"]
)
age_fig.update_layout(showlegend=False)
age_fig = style_figure(age_fig)


gender_fig = px.pie(
    gender_distribution,
    names="sex",
    values="patient_count",
    hole=0.45,
    title="Gender Distribution",
    color_discrete_sequence=["#1F77B4", "#F0AD4E"]
)
gender_fig = style_figure(gender_fig)


heatmap_fig = go.Figure(
    data=go.Heatmap(
        z=dept_risk_pivot[["Critical", "High Risk", "Routine"]].values,
        x=["Critical", "High Risk", "Routine"],
        y=dept_risk_pivot["department_name"],
        colorscale=[
            [0, "#F4F6F9"],
            [0.5, "#F0AD4E"],
            [1, "#D9534F"]
        ],
        text=dept_risk_pivot[["Critical", "High Risk", "Routine"]].values,
        texttemplate="%{text}",
        textfont={"size": 12},
        colorbar=dict(title="Count")
    )
)

heatmap_fig.update_layout(
    title="Department Risk Heatmap",
    template="plotly_white",
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(family="Segoe UI, Arial", size=12, color="#263238"),
    margin=dict(l=90, r=20, t=55, b=35)
)


app = Dash(__name__)
app.title = "LabRisk Clinical Monitoring Dashboard"


page_style = {
    "fontFamily": "Segoe UI, Arial",
    "backgroundColor": "#F4F6F9",
    "padding": "22px"
}

header_style = {
    "background": "linear-gradient(90deg, #061B3A, #0B3A66)",
    "color": "white",
    "padding": "24px 28px",
    "borderRadius": "16px",
    "boxShadow": "0 4px 14px rgba(0,0,0,0.16)",
    "marginBottom": "22px"
}

card_style = {
    "backgroundColor": "white",
    "padding": "18px",
    "borderRadius": "14px",
    "boxShadow": "0 2px 10px rgba(0,0,0,0.08)",
    "textAlign": "center",
    "borderTop": "5px solid #1F77B4"
}

critical_card_style = {
    **card_style,
    "borderTop": "5px solid #D9534F"
}

warning_card_style = {
    **card_style,
    "borderTop": "5px solid #F0AD4E"
}

safe_card_style = {
    **card_style,
    "borderTop": "5px solid #5CB85C"
}

section_style = {
    "backgroundColor": "white",
    "borderRadius": "14px",
    "boxShadow": "0 2px 10px rgba(0,0,0,0.08)",
    "padding": "8px"
}


def kpi_card(title, value, style):
    return html.Div(
        style=style,
        children=[
            html.Div(
                title,
                style={
                    "fontSize": "13px",
                    "fontWeight": "600",
                    "color": "#5F6B7A",
                    "textTransform": "uppercase"
                }
            ),
            html.Div(
                value,
                style={
                    "fontSize": "30px",
                    "fontWeight": "800",
                    "color": "#0B1F3A",
                    "marginTop": "8px"
                }
            )
        ]
    )


app.layout = html.Div(
    style=page_style,
    children=[
        html.Div(
            style=header_style,
            children=[
                html.Div(
                    "LABRISK CLINICAL DASHBOARD",
                    style={
                        "fontSize": "30px",
                        "fontWeight": "800",
                        "letterSpacing": "1px"
                    }
                ),
                html.Div(
                    "Healthcare laboratory monitoring | SQL Server warehouse | ETL validation | Operational alerting and clinical escalation",
                    style={
                        "fontSize": "15px",
                        "opacity": "0.9",
                        "marginTop": "6px"
                    }
                )
            ]
        ),

        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(6, 1fr)",
                "gap": "16px",
                "marginBottom": "22px"
            },
            children=[
                kpi_card("Total Lab Results", f"{total_lab_results:,}", card_style),
                kpi_card("Total Patients", f"{total_patients:,}", card_style),
                kpi_card("Abnormal Results", f"{abnormal_results:,}", warning_card_style),
                kpi_card("Critical Results", f"{critical_results:,}", critical_card_style),
                kpi_card("High Risk Results", f"{high_risk_results:,}", warning_card_style),
                kpi_card("Departments", f"{departments_monitored:,}", safe_card_style),
            ]
        ),

        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "1fr 1.4fr",
                "gap": "20px",
                "marginBottom": "20px"
            },
            children=[
                html.Div(dcc.Graph(figure=risk_fig), style=section_style),
                html.Div(dcc.Graph(figure=trend_fig), style=section_style),
            ]
        ),

        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "1fr 1fr",
                "gap": "20px",
                "marginBottom": "20px"
            },
            children=[
                html.Div(dcc.Graph(figure=lab_dept_fig), style=section_style),
                html.Div(dcc.Graph(figure=critical_dept_fig), style=section_style),
            ]
        ),

        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "1.2fr 1fr",
                "gap": "20px",
                "marginBottom": "20px"
            },
            children=[
                html.Div(dcc.Graph(figure=heatmap_fig), style=section_style),
                html.Div(
                    style={
                        "display": "grid",
                        "gridTemplateRows": "1fr 1fr",
                        "gap": "20px"
                    },
                    children=[
                        html.Div(dcc.Graph(figure=age_fig), style=section_style),
                        html.Div(dcc.Graph(figure=gender_fig), style=section_style),
                    ]
                )
            ]
        ),

        html.Div(
            style={
                "marginBottom": "20px"
            },
            children=[
                html.Div(dcc.Graph(figure=diagnosis_fig), style=section_style)
            ]
        ),

        html.Div(
            style={
                "backgroundColor": "white",
                "padding": "18px",
                "borderRadius": "14px",
                "boxShadow": "0 2px 10px rgba(0,0,0,0.08)"
            },
            children=[
                html.Div(
                    "High Risk Patient Monitoring",
                    style={
                        "fontSize": "20px",
                        "fontWeight": "800",
                        "color": "#0B1F3A",
                        "marginBottom": "12px"
                    }
                ),
                dash_table.DataTable(
                    data=high_risk_table.to_dict("records"),
                    columns=[
                        {"name": column.replace("_", " ").title(), "id": column}
                        for column in high_risk_table.columns
                    ],
                    page_size=10,
                    style_table={"overflowX": "auto"},
                    style_cell={
                        "textAlign": "left",
                        "padding": "9px",
                        "fontFamily": "Segoe UI",
                        "fontSize": "12px",
                        "border": "1px solid #E6EAF0"
                    },
                    style_header={
                        "backgroundColor": "#061B3A",
                        "color": "white",
                        "fontWeight": "bold",
                        "border": "1px solid #061B3A"
                    },
                    style_data_conditional=[
                        {
                            "if": {"filter_query": "{risk_level} = 'Critical'"},
                            "backgroundColor": "#F8D7DA",
                            "color": "#721C24"
                        },
                        {
                            "if": {"filter_query": "{risk_level} = 'High Risk'"},
                            "backgroundColor": "#FFF3CD",
                            "color": "#856404"
                        }
                    ],
                    sort_action="native",
                    filter_action="native"
                )
            ]
        )
    ]
)


if __name__ == "__main__":
    app.run(debug=True)