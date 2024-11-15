import pandas as pd
import numpy as np
import numpy_financial as npf

def calculate(df):
    # Ensure 'Target Pay' is numeric and 'Grade' is integer
    df['Target Pay'] = pd.to_numeric(df['Target Pay'], errors='coerce')
    df['Grade'] = pd.to_numeric(df['Grade'], errors='coerce').astype(int)

    # Function to calculate midpoint differential using RATE formula
    def calculate_midpoint_differential(df):
        max_grade = df['Grade'].max()
        min_grade = df['Grade'].min()
        highest_midpoint = df[df['Grade'] == max_grade]['Target Pay'].values[0]
        lowest_midpoint = df[df['Grade'] == min_grade]['Target Pay'].values[0]
        nper = max_grade - min_grade
        pv = -lowest_midpoint
        fv = highest_midpoint
        midpoint_differential = npf.rate(nper, 0, pv, fv)
        return midpoint_differential

    # Function to interpolate missing grades using the midpoint differential
    def interpolate_missing_grades(df):
        # Calculate midpoint differential
        midpoint_differential = calculate_midpoint_differential(df)

        # Get the range of grades
        min_grade = df['Grade'].min()
        max_grade = df['Grade'].max()

        # Initialize an empty list to store interpolated rows
        interpolated_rows = []

        # Iterate over the range of grades to identify and fill missing grades
        for grade in range(min_grade, max_grade + 1):
            if grade not in df['Grade'].values:
                lower_grade = df[df['Grade'] < grade]['Grade'].max()
                lower_grade_avg = df[df['Grade'] == lower_grade]['Target Pay'].values[0]
                missing_grade_avg = lower_grade_avg * (1 + midpoint_differential)
                interpolated_rows.append({'Grade': grade, 'Target Pay': missing_grade_avg})

        # Create a DataFrame from the interpolated rows
        interpolated_df = pd.DataFrame(interpolated_rows)

        # Concatenate the original DataFrame and the interpolated DataFrame
        result_df = pd.concat([df, interpolated_df]).sort_values(by='Grade').reset_index(drop=True)

        return result_df

    # Apply interpolation
    result_df = interpolate_missing_grades(df)

    # Calculate range minimum and maximum (using a fixed 30% spread for this example)
    result_df['Range Minimum'] = result_df['Target Pay'] * 0.85
    result_df['Range Maximum'] = result_df['Target Pay'] * 1.15

    # Calculate range spread
    result_df['Range Spread'] = (result_df['Range Maximum'] / result_df['Range Minimum']) - 1

    # Calculate MPD (Midpoint Differential)
    result_df['MPD'] = result_df['Target Pay'].pct_change()
    result_df['Mid Pnt Diff'] = result_df['MPD'].apply(lambda x: '-' if pd.isna(x) else f'{x:.1%}')

    # Drop the 'MPD' column
    result_df.drop(columns=['MPD'], inplace=True)

    # Rename columns
    result_df.rename(columns={'Target Pay': 'Range Mid'}, inplace=True)

    # Reorder columns
    result_df = result_df[['Grade', 'Range Minimum', 'Range Mid', 'Range Maximum', 'Mid Pnt Diff', 'Range Spread']]

    # Format the numeric columns
    for col in ['Range Minimum', 'Range Mid', 'Range Maximum']:
        result_df[col] = result_df[col].apply(lambda x: '{:,.0f}'.format(x))
    result_df['Range Spread'] = (result_df['Range Spread'] * 100).round(1).astype(str) + '%'


# Drop the index from the DataFrame
    result_df.reset_index(drop=True, inplace=True)

# Extract unique values from the "Grade" column and their corresponding values
    result_df.drop_duplicates(subset='Grade')

    return result_df