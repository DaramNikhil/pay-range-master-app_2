import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.io as pio

def analyze_salary_distribution(df, min_employees_per_grade=2, output_csv=r'artifacts\option_2.csv'):
  # Ensure correct data types
  df['Base Pay'] = pd.to_numeric(df['Base Pay'], errors='coerce')
  df['Grade'] = pd.to_numeric(df['Grade'], errors='coerce').astype('Int64')
  df = df.dropna(subset=['Base Pay', 'Grade'])

  # Get list of all grades
  all_grades = pd.DataFrame({'Grade': range(df['Grade'].min(), df['Grade'].max() + 1)})

  # Calculate Mid values for grades with sufficient data
  def find_optimal_mid(group):
      salaries = group['Base Pay'].dropna().values
      if len(salaries) >= min_employees_per_grade:
          candidate_mids = np.linspace(salaries.min(), salaries.max(), 1000)
          max_count = 0
          optimal_mid = salaries.mean()
          for mid in candidate_mids:
              lower_bound = 0.8 * mid
              upper_bound = 1.2 * mid
              count = np.sum((salaries >= lower_bound) & (salaries <= upper_bound))
              if count > max_count:
                  max_count = count
                  optimal_mid = mid
          return optimal_mid
      else:
          return np.nan  # Insufficient data; will be interpolated

  # Apply the function to each grade
  mids = df.groupby('Grade').apply(find_optimal_mid).reset_index()
  mids.columns = ['Grade', 'Mid']

  # Merge with all grades to ensure all grades are included
  mids = pd.merge(all_grades, mids, on='Grade', how='left')

  # Flag to indicate how Mid was calculated
  mids['Mid_Calculation'] = np.where(mids['Mid'].notna(), 'Calculated', 'Interpolated')

  # Interpolate missing Mids
  mids['Mid'] = mids['Mid'].interpolate(method='linear', limit_direction='both')

  # Ensure that higher grades have higher Mids
  mids.sort_values('Grade', inplace=True)
  mids.reset_index(drop=True, inplace=True)

  for i in range(1, len(mids)):
      if mids.at[i, 'Mid'] <= mids.at[i - 1, 'Mid']:
          # Compute 3% increase over previous Mid
          increment_3_percent = 0.03 * mids.at[i - 1, 'Mid']
          increments = [increment_3_percent]

          # Check if there's an upper grade to calculate half midpoint differential
          if i + 1 < len(mids):
              midpoint_diff = mids.at[i + 1, 'Mid'] - mids.at[i - 1, 'Mid']
              half_midpoint_diff = midpoint_diff / 2
              if half_midpoint_diff > 0:
                  increments.append(half_midpoint_diff)

          # Determine the minimum positive increment
          positive_increments = [inc for inc in increments if inc > 0]
          if positive_increments:
              min_increment = min(positive_increments)
          else:
              # Default to a small positive increment to ensure increasing Mid
              min_increment = .3 * mids.at[i - 1, 'Mid']

          # Adjust Mid_current
          mids.at[i, 'Mid'] = mids.at[i - 1, 'Mid'] + min_increment
          mids.at[i, 'Mid_Calculation'] = 'Adjusted'

  # Calculate Range_Min and Range_Max
  mids['Range_Min'] = 0.8 * mids['Mid']
  mids['Range_Max'] = 1.2 * mids['Mid']

  # Calculate Spread
  mids['Spread'] = ((mids['Range_Max'] - mids['Range_Min']) / mids['Range_Min']) * 100

  # Calculate Mid-point Differential
  mids.sort_values('Grade', ascending=False, inplace=True)
  mids['Mid_Pnt_Diff'] = (mids['Mid'] / mids['Mid'].shift(-1) - 1) * 100
  mids['Mid_Pnt_Diff'] = mids['Mid_Pnt_Diff'].round(2).astype(str).replace('nan', '')

  # Rounding
  mids['Range_Min'] = mids['Range_Min'].round(0).astype(int)
  mids['Mid'] = mids['Mid'].round(0).astype(int)
  mids['Range_Max'] = mids['Range_Max'].round(0).astype(int)
  mids['Spread'] = mids['Spread'].round(2)

  
  mids.sort_values('Grade', ascending=False, inplace=True)
  mids['Range_Overlap'] = (mids['Range_Max'].shift(-1) / mids['Range_Min']) - 1
  mids['Range_Overlap'] = (mids['Range_Overlap'] * 100).round(2)
  mids['Range_Overlap'] = mids['Range_Overlap'].fillna('')

  
  result_df = mids[['Grade', 'Range_Min', 'Mid', 'Range_Max', 'Spread', 'Mid_Pnt_Diff', 'Range_Overlap']]

  result_df.to_csv(output_csv, index=False)
  access_df_2 = pd.read_csv(output_csv)
  return access_df_2