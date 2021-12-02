import dash
from dash import dash_table
from dash import dcc # dash core components
from dash import html

from dash.dependencies import Input, Output

import pandas as pd

df = pd.read_csv('https://bit.ly/elements-periodic-table')

# create columns that have unique values
unique_col = ["AtomicNumber", "Element", "Symbol", "NumberOfProtons", "NumberOfElectrons"]

# create columns that don't have unique values
not_unique_col = ['AtomicMass', 'NumberOfNeutrons', 'Period', 'Group', 'Phase', 'Radioactive', 'Natural', 'Metal', 'Nonmetal',
                  'Metalloid', 'Type', 'AtomicRadius', 'Electronegativity', 'FirstIonization', 'Density', 'MeltingPoint',
                  'BoilingPoint', 'NumberOfIsotopes', 'Discoverer', 'Year', 'SpecificHeat', 'NumberOfShells', 'NumberOfValence']

app = dash.Dash(__name__)

# make app layout
app.layout = html.Div([
   html.Div([
      dcc.Dropdown(
      id='index_selection',
      options=[{'label': col, 'value': col} for col in unique_col],
      value=None
      )
   ]),
   html.Div(id='index-output'),
   html.Div([
      dcc.Dropdown(
      id='column_selection',
      options=[{'label': col, 'value': col} for col in unique_col],
      value=None
      )
   ]),
   html.Div(id='column-output'),
   html.Div([
      dcc.Dropdown(
      id='value_selection',
      options=[{'label': col, 'value': col} for col in not_unique_col],
      value=None
      )
   ]),
   html.Div(id='value-output'),
   html.Div([
      dash_table.DataTable(
      id='pivot-table',
      columns=[{"name": i, "id": i} for i in df.columns],
      data=df.to_dict('records')
      )
   ])
])

# app callback
@app.callback(
   Output(component_id='pivot_table', component_property='data'),
   [
      Input(component_id='index_selection', component_property='value'),
      Input(component_id='column_selection', component_property='value'),
      Input(component_id='value_selection', component_property='value')
   ]
)

# make an identity function
def identity(x): return x

# make function to make pivot table
def output_table(df, index_col, columns_col, values_col):
   not_unique_cols = [ col for col in df.columns if df[col].is_unique == False]
   if index_col == columns_col or index_col == values_col or columns_col ==values_col:
      print("row and column index needs to be different")
   else:
      df_piv = df.pivot_table(
            index= index_col,
            columns= columns_col,
            values= values_col,
            aggfunc=identity,
      )
      return df_piv

# run app
app.run_server(debug=True, host="0.0.0.0")

