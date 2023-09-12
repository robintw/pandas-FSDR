# Pandas Find Significantly Different Rows (pandas-FSDR)

This is a relatively simple function that finds rows in a pandas
DataFrame where the values in two columns are significantly
different. Significantly different in this context means that the
values have a relative or absolute difference greater than a
threshold. By default this function returns a chunk of
human-readable text describing the differences.

For example, given a DataFrame of:

```
              UK  World
Biology      50     40
Geography    75     80
Computing   100     50
Maths      1500   1600
```

and a relative difference threshold of 30% (the default) and an absolute
difference threshold of 75, this function would return the following text:

  - Maths is significantly smaller for UK (1500 for UK compared to
  1600 for World)
  - Computing is significantly larger for UK (100 for UK compared to
  50 for World)

This output is easily configurable using the various parameters
(described below).

I wrote this when doing some data analysis for a client many years ago, and thought it would be worth sharing.

### Example
```
# Set up some sample data
df = pd.DataFrame({'UK':[50, 75, 100, 1500],
                   'World': [40, 80, 50, 1600]},
                   index=['Biology', 'Geography', 'Computing', 'Maths'])
print(df)

result = FSDR(df, 'UK', 'World', rel_thresh=30, abs_thresh=75)

print(result)

# Prints:
#
# - **Maths** is significantly __smaller__ for UK (1500 for UK compared to 1600 for World)
# - **Computing** is significantly __larger__ for UK (100 for UK compared to 50 for World)
#

```

### Full documentation

There is just one function, called `FSDR` with the parameters below:

  - `df`: the pandas DataFrame to process
  - `main_col`: the column to compare values in. Percentage differences will be
    calculated relative to this column.
  - `other_col`: the column to compare values to (ie. the 'other column' to
  main_col)
  - `rel_thresh`: the threshold above which a relative difference is
  considered significant, in percent.
    To set no relative threshold set to None. (Default: 30)
  - `abs_thresh`: the threshold above which an absolute difference is
  considered significant. To set no
    absolute threshold set to None. (Default: None)
  - `return_text`: Set to True to return human-readable text descriptions of
  the significant differences.
    If False then return a list of row index values for rows which have
    significant differences. (Default: True)
  - `markdown`: Set to True to return Markdown formatted text, wrapped in a
  Markdown display object for display in the Jupyter notebook. If False,
  returns plain text. (Default: True)
  - `value_suffix`: A string to be appended to each value in the resulting
  text output. For example, allows
    all values to be followed by % if they are percentages. (Default: '')
  - `comparison_text_larger`: A string to be used in the text output when
  describing a value that is larger than another value. (Default: 'larger')
  - `comparison_text_smaller`: A string to be used in the text output when
  describing a value that is smaller than another value. (Default: 'smaller')
  - `value_format_str`: A format string used to format values when included
  in the text output. For example: '.2f' for floating point numbers with
  two decimal places. (Default: '')
  - `intro_text`: Text to be included before the list of significant
  differences. For proper markdown formatting this should end in '\n\n'.
  (Default: '')
  - `min_value`: Minimum value (of either main_col or other_col) to be used
  when calculating significant differences. All rows with values lower
  than this will be excluded from all calculations. Set to None to disable
  minimum value checking. (Default: None)

Returns:
    A chunk of human-readable text describing significant differences in
    the DataFrame (by default, if `return_text` is True). Otherwise, return
    a list of index values for rows where there are significant
    differences.