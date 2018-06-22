import pandas as pd

try:
    from IPython.display import Markdown
except ImportError:
    Markdown = lambda x: x

def FSDR(df, main_col, other_col, rel_thresh=30, abs_thresh=None, return_text=True, markdown=True,
         value_suffix="", comparison_text_larger='larger', comparison_text_smaller='smaller',
         value_format_str='', intro_text="",
         min_value=None):
    """
    Find Significantly Different Rows (FSDR): finds rows in a pandas DataFrame where the values in
    two columns are significantly different. Significantly different in this context means that the values
    have a relative or absolute difference greater than a threshold. By default this function returns a
    chunk of human-readable text describing the differences.

    For example, given a DataFrame of:

                 UK  World
    Biology      50     40
    Geography    75     80
    Computing   100     50
    Maths      1500   1600

    and a relative difference threshold of 30% (the default) and an absolute difference threshold of 75,
    this function would return the following text:

     - Maths is significantly smaller for UK (1500 for UK compared to 1600 for World)
     - Computing is significantly larger for UK (100 for UK compared to 50 for World)

     This output is easily configurable using the various parameters (described below).

     Parameters:

      - df: the pandas DataFrame to process
      - main_col: the column to compare values in. Percentage differences will be
        calculated relative to this column.
      - other_col: the column to compare values to (ie. the 'other column' to main_col
      - rel_thresh: the threshold above which a relative difference is considered significant, in percent.
        To set no relative threshold set to None. (Default: 30)
      - abs_thresh: the threshold above which an absolute difference is considered significant. To set no
        absolute threshold set to None. (Default: None)
      - return_text: Set to True to return human-readable text descriptions of the significant differences.
        If False then return a list of row index values for rows which have significant differences. (Default: True)
      - markdown: Set to True to return Markdown formatted text, wrapped in a Markdown display object for
        display in the Jupyter notebook. If False, returns plain text. (Default: True)
      - value_suffix: A string to be appended to each value in the resulting text output. For example, allows
        all values to be followed by % if they are percentages. (Default: '')
      - comparison_text_larger: A string to be used in the text output when describing a value that is larger
        than another value. (Default: 'larger')
      - comparison_text_smaller: A string to be used in the text output when describing a value that is smaller
        than another value. (Default: 'smaller')
      - value_format_str: A format string used to format values when included in the text output. For example:
        '.2f' for floating point numbers with two decimal places. (Default: '')
      - intro_text: Text to be included before the list of significant differences. For proper markdown
        formatting this should end in '\n\n'. (Default: '')
      - min_value: Minimum value (of either main_col or other_col) to be used when calculating significant
        differences. All rows with values lower than this will be excluded from all calculations. Set to None
        to disable minimum value checking. (Default: None)

    Returns:
        A chunk of human-readable text describing significant differences in the DataFrame (by default, if return_text
        is True). Otherwise, return a list of index values for rows where there are significant differences.

    """
    # Copy df so any changes we make aren't propagated back to the calling function
    df = df.copy()

    if min_value is not None:
        max_val = df.max(axis=1)
        df = df[max_val > min_value]
    
    # Calculate difference, absolute difference and percentage difference (relative to main_col)
    diff = df[main_col] - df[other_col]
    abs_diff = diff.abs()
    perc_diff = (abs_diff / df[main_col]) * 100
    
    # Calculate rows that are significantly different because the percentage difference is over the relative threshold
    if rel_thresh is not None:
        sig_diff_by_perc = set(perc_diff[perc_diff > rel_thresh].index)
    else:
        sig_diff_by_perc = set()
    
    # Calculate rows that are significantly different because the absolute difference is over the absolute threshold
    if abs_thresh is not None:
        sig_diff_by_abs = set(abs_diff[abs_diff > abs_thresh].index)
    else:
        sig_diff_by_abs = set()
    
    # Union these two to get *all* significantly different rows
    sig_diff_rows = sig_diff_by_perc.union(sig_diff_by_abs)
    
    # If we don't want the text (just the row indexes) then return now
    if not return_text:
        return list(sig_diff_rows)
    
    # Get the subset of the data frame that contains the significantly different rows
    # and sort descending by the values in main_col - so that we get the biggest ones at the top
    just_sig_rows = df.loc[list(sig_diff_rows)]
    just_sig_rows = just_sig_rows.sort_values(main_col, ascending=False)
    
    output_text = intro_text
    
    # Iterate through the rows and generate the text according to the template
    for item, row in just_sig_rows.iterrows():
        main_val = row[main_col]
        other_val = row[other_col]
        
        if main_val > other_val:
            comparison_text = comparison_text_larger
        else:
            comparison_text = comparison_text_smaller
        
        if markdown:
            italics = "_"
            bold = "**"
        else:
            italics = ""
            bold = ""

        row = (f' - {bold}{item}{bold} is significantly {italics}{comparison_text}{italics} for {main_col} '
               f'({main_val:{value_format_str}}{value_suffix} for {main_col} '
               f'compared to {other_val:{value_format_str}}{value_suffix} for {other_col})\n')
        
        output_text += row
    
    if markdown:
        return Markdown(output_text)
    else:
        return output_text