import pyodbc
import pandas as pd
from dash import Dash, html, dcc, dash_table, Input, Output
import plotly.express as px


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
        LEFT JOIN encounters e ON lr.encounter_id = e.encounter_id
        LEFT JOIN patients p ON e.patient_id = p.patient_id
        LEFT JOIN diagnoses d ON e.diagnosis_code = d.diagnosis_code
        LEFT JOIN departments dept ON e.department_id = dept.department_id
        LEFT JOIN providers pr ON e.provider_id = pr.provider_id
        LEFT JOIN lab_tests lt ON lr.lab_test_id = lt.lab_test_id;
    """

    connection = pyodbc.connect(connection_string)
    df = pd.read_sql(query, connection)
    connection.close()

    df["result_date"] = pd.to_datetime(df["result_date"])
    return df


df = load_dashboard_data()


app = Dash(__name__)
app.title = "LabRisk Clinical Dashboard"


risk_colors = {
    "Critical": "#D71920",
    "High Risk": "#FF9800",
    "Routine": "#2EAD4B"
}


def dropdown_options(series):
    return [{"label": x, "value": x} for x in sorted(series.dropna().unique())]


def kpi_card(title, value, color="#005BBB"):
    return html.Div(
        style={
            "backgroundColor": "white",
            "borderRadius": "14px",
            "padding": "16px",
            "boxShadow": "0 2px 8px rgba(0,0,0,0.12)",
            "borderTop": f"5px solid {color}",
            "textAlign": "center"
        },
        children=[
            html.Div(title, style={"fontSize": "12px", "fontWeight": "700", "color": "#0B1F3A"}),
            html.Div(value, style={"fontSize": "30px", "fontWeight": "800", "color": color})
        ]
    )


app.layout = html.Div(
    style={"fontFamily": "Segoe UI", "backgroundColor": "#F4F6F9", "padding": "18px"},
    children=[
        html.Div(
            style={
                "background": "linear-gradient(90deg, #061B3A, #0B3A66)",
                "color": "white",
                "padding": "22px",
                "borderRadius": "14px",
                "marginBottom": "18px"
            },
            children=[
                html.H1("LABRISK CLINICAL DASHBOARD", style={"margin": "0"}),
                html.P("Hospital Laboratory Monitoring & Risk Intelligence System")
            ]
        ),

        html.Div(
            style={"display": "grid", "gridTemplateColumns": "220px 1fr", "gap": "18px"},
            children=[
                html.Div(
                    style={
                        "backgroundColor": "white",
                        "borderRadius": "14px",
                        "padding": "16px",
                        "boxShadow": "0 2px 8px rgba(0,0,0,0.12)"
                    },
                    children=[
                        html.H3("FILTERS", style={"color": "#0B1F3A"}),

                        html.Label("Department"),
                        dcc.Dropdown(
                            id="department-filter",
                            options=dropdown_options(df["department_name"]),
                            multi=True
                        ),

                        html.Br(),

                        html.Label("Diagnosis"),
                        dcc.Dropdown(
                            id="diagnosis-filter",
                            options=dropdown_options(df["diagnosis_name"]),
                            multi=True
                        ),

                        html.Br(),

                        html.Label("Risk Level"),
                        dcc.Dropdown(
                            id="risk-filter",
                            options=dropdown_options(df["risk_level"]),
                            multi=True
                        ),

                        html.Br(),

                        html.Label("Gender"),
                        dcc.Dropdown(
                            id="gender-filter",
                            options=dropdown_options(df["sex"]),
                            multi=True
                        ),

                        html.Br(),

                        html.Label("Lab Test"),
                        dcc.Dropdown(
                            id="lab-test-filter",
                            options=dropdown_options(df["lab_test_name"]),
                            multi=True
                        ),

                        html.Br(),

                        html.Label("Date Range"),
                        dcc.DatePickerRange(
                            id="date-filter",
                            min_date_allowed=df["result_date"].min(),
                            max_date_allowed=df["result_date"].max(),
                            start_date=df["result_date"].min(),
                            end_date=df["result_date"].max(),
                            display_format="MM/DD/YYYY"
                        )
                    ]
                ),

                html.Div(
                    children=[
                        html.Div(
                            id="kpi-row",
                            style={
                                "display": "grid",
                                "gridTemplateColumns": "repeat(6, 1fr)",
                                "gap": "14px",
                                "marginBottom": "16px"
                            }
                        ),

                        html.Div(
                            style={"display": "grid", "gridTemplateColumns": "1fr 1.4fr", "gap": "16px"},
                            children=[
                                dcc.Graph(id="risk-distribution"),
                                dcc.Graph(id="risk-trend")
                            ]
                        ),

                        html.Div(
                            style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "16px"},
                            children=[
                                dcc.Graph(id="lab-by-department"),
                                dcc.Graph(id="critical-by-department")
                            ]
                        ),

                        html.Div(
                            style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "16px"},
                            children=[
                                dcc.Graph(id="diagnosis-distribution"),
                                dcc.Graph(id="age-distribution")
                            ]
                        ),

                        html.Div(
                            style={
                                "backgroundColor": "white",
                                "borderRadius": "14px",
                                "padding": "16px",
                                "boxShadow": "0 2px 8px rgba(0,0,0,0.12)"
                            },
                            children=[
                                html.H3("High Risk Patient Monitoring", style={"color": "#0B1F3A"}),
                                dash_table.DataTable(
                                    id="patient-table",
                                    page_size=10,
                                    filter_action="native",
                                    sort_action="native",
                                    style_table={"overflowX": "auto"},
                                    style_header={
                                        "backgroundColor": "#061B3A",
                                        "color": "white",
                                        "fontWeight": "bold"
                                    },
                                    style_cell={
                                        "fontFamily": "Segoe UI",
                                        "fontSize": "12px",
                                        "padding": "8px",
                                        "textAlign": "left"
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
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)


@app.callback(
    [
        Output("kpi-row", "children"),
        Output("risk-distribution", "figure"),
        Output("risk-trend", "figure"),
        Output("lab-by-department", "figure"),
        Output("critical-by-department", "figure"),
        Output("diagnosis-distribution", "figure"),
        Output("age-distribution", "figure"),
        Output("patient-table", "data"),
        Output("patient-table", "columns")
    ],
    [
        Input("department-filter", "value"),
        Input("diagnosis-filter", "value"),
        Input("risk-filter", "value"),
        Input("gender-filter", "value"),
        Input("lab-test-filter", "value"),
        Input("date-filter", "start_date"),
        Input("date-filter", "end_date")
    ]
)
def update_dashboard(departments, diagnoses, risks, genders, lab_tests, start_date, end_date):
    filtered = df.copy()

    if departments:
        filtered = filtered[filtered["department_name"].isin(departments)]

    if diagnoses:
        filtered = filtered[filtered["diagnosis_name"].isin(diagnoses)]

    if risks:
        filtered = filtered[filtered["risk_level"].isin(risks)]

    if genders:
        filtered = filtered[filtered["sex"].isin(genders)]

    if lab_tests:
        filtered = filtered[filtered["lab_test_name"].isin(lab_tests)]

    filtered = filtered[
        (filtered["result_date"] >= pd.to_datetime(start_date)) &
        (filtered["result_date"] <= pd.to_datetime(end_date))
    ]

    total_lab_results = len(filtered)
    total_patients = filtered["patient_id"].nunique()
    abnormal_results = len(filtered[filtered["result_status"] != "Normal"])
    critical_results = len(filtered[filtered["risk_level"] == "Critical"])
    high_risk_results = len(filtered[filtered["risk_level"] == "High Risk"])
    departments_monitored = filtered["department_name"].nunique()

    kpis = [
        kpi_card("Total Lab Results", f"{total_lab_results:,}", "#005BBB"),
        kpi_card("Total Patients", f"{total_patients:,}", "#005BBB"),
        kpi_card("Abnormal Results", f"{abnormal_results:,}", "#E87500"),
        kpi_card("Critical Results", f"{critical_results:,}", "#D71920"),
        kpi_card("High Risk Results", f"{high_risk_results:,}", "#FF9800"),
        kpi_card("Departments", f"{departments_monitored:,}", "#2EAD4B"),
    ]

    risk_counts = filtered.groupby("risk_level").size().reset_index(name="count")

    risk_fig = px.pie(
        risk_counts,
        names="risk_level",
        values="count",
        hole=0.55,
        title="Risk Level Distribution",
        color="risk_level",
        color_discrete_map=risk_colors
    )

    trend_data = filtered.groupby(["result_date", "risk_level"]).size().reset_index(name="count")

    trend_fig = px.line(
        trend_data,
        x="result_date",
        y="count",
        color="risk_level",
        markers=True,
        title="Lab Results Trend by Risk Level",
        color_discrete_map=risk_colors
    )

    lab_dept = (
        filtered.groupby("department_name")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=True)
    )

    lab_dept_fig = px.bar(
        lab_dept,
        x="count",
        y="department_name",
        orientation="h",
        title="Lab Results by Department"
    )

    critical_dept = (
        filtered[filtered["risk_level"] == "Critical"]
        .groupby("department_name")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=True)
    )

    critical_fig = px.bar(
        critical_dept,
        x="count",
        y="department_name",
        orientation="h",
        title="Critical Results by Department"
    )

    diagnosis = (
        filtered.groupby("diagnosis_name")
        .size()
        .reset_index(name="count")
    )

    diagnosis_fig = px.treemap(
        diagnosis,
        path=["diagnosis_name"],
        values="count",
        title="Diagnosis Distribution"
    )

    age_df = filtered.drop_duplicates("patient_id").copy()

    age_df["age_group"] = pd.cut(
        age_df["age"],
        bins=[18, 30, 45, 60, 75, 100],
        labels=["18-30", "31-45", "46-60", "61-75", "76+"],
        include_lowest=True
    )

    age_grouped = age_df.groupby("age_group", observed=False).size().reset_index(name="count")

    age_fig = px.bar(
        age_grouped,
        x="age_group",
        y="count",
        title="Age Distribution"
    )

    table_df = filtered[
        filtered["risk_level"].isin(["Critical", "High Risk"])
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

    table_df["result_date"] = table_df["result_date"].dt.strftime("%m/%d/%Y")

    columns = [
        {"name": col.replace("_", " ").title(), "id": col}
        for col in table_df.columns
    ]

    return (
        kpis,
        risk_fig,
        trend_fig,
        lab_dept_fig,
        critical_fig,
        diagnosis_fig,
        age_fig,
        table_df.to_dict("records"),
        columns
    )


if __name__ == "__main__":
    app.run(debug=True)