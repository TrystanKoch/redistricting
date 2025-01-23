"""For splitting regions into districts recursively."""

def horizontal_splitter(region_block_centroids, max_small_district_population):
    """Splits a region in two, by population, horizontally.

    Splits a region into two, horizontally. The smaller region will have a 
    population that is as large as possible while still being less than a 
    given population.

    Parameters
    ----------
    region_block_centroids : pandas.core.frame.DataFrame
        A dataframe that corresponds to a region
    max_small_district_population : int
        A population maximum for the smaller of the resulting districts

    Returns
    -------
    pandas.core.frame.DataFrame
        A mask that is true for all blocks part of the smaller region
    """
    # This naive test function only splits the state in horizontal lines.
    # Because of this, the angular step is always 0, corresponding to
    # lines that are horizontal in our gnomonic CRS.
    # Note: this IS a great circle. This IS NOT a line of latitude.
    step = 0

    return (
        # This should be one of our cleaned centroid blocks.
        region_block_centroids

        # Sort by the column that corresponds to distance along a specified
        # direction. The directions are labeled by the angular step we are on.
        .sort_values([str(step)])

        # Find the cumulative sum of the population. This is equivalent to
        # slowly moving our dividing line in the direction normal to the
        # angluar step we chose, then finding how much of our population is
        # behind that line.
        ["POP20"].cumsum()

        # Finally, create a mask which is true only if that cumulative sum is
        # less than our specified maximum population
        < max_small_district_population
    )


def split_district(cb_blocks, region_mask, num_districts, district_count):
    """Recursively split a region into districts of almost equal population.

    Recursively split a region into districts with populations in proportion 
    to an even split of districts.

    Parameters
    ----------
    cb_blocks : geopandas.geodataframe.GeoDataFrame
        A (mutating!) dataframe representing census blocks
    region_mask : pandas.core.frame.DataFrame
        A mask over the census blocks, indicating the current region to split
    num_districts : int
        The total number of districts we want to split the state into
    district_count : int
        The number of districts we have created so far
    """

    # Find the total population of the district
    total_population = cb_blocks.mask(~region_mask)["POP20"].sum()

    # If there's only one district to label, label it using the latest label.
    # Tell the user that we found it. Our recursive base case.
    if num_districts == 1:
        district_count += 1
        cb_blocks.loc[region_mask, "district"] = district_count
        print(
            f"Created district {district_count},",
            f"population {total_population}."
        )
        return district_count

    # At this point, we know that we have to split our current region at least
    # one time. Determine how many divisions will need to be made in each
    # branch after the next split.
    small_district_divisions = num_districts // 2
    large_district_divisions = num_districts - (small_district_divisions)

    # We'll need this to determine the population cutoff for our split. The
    # next two regions should have populations in the same ratio as their
    # numbers of districts.
    small_district_proportion = small_district_divisions / num_districts
    small_district_population = total_population * small_district_proportion

    # Split the district with a splitting function.
    # Note that we assume our function returns a mask for the smaller of the
    # two regions.
    small_district_mask = horizontal_splitter(
        cb_blocks.mask(~region_mask),
        small_district_population
    )

    # Recurse using the smaller district.
    district_count = split_district(
        cb_blocks,
        small_district_mask,
        small_district_divisions,
        district_count
    )

    # Recurse using the larger district.
    district_count = split_district(
        cb_blocks,
        region_mask & ~small_district_mask,
        large_district_divisions,
        district_count
    )

    return district_count


def split_state(block_centroids, num_districts):
    """Splits census blocks into districts of almost equal population.

    Recursively splits a region into districts of equal population in place.

    Parameters
    ----------
    block_centroids:geopandas.geoframe.GeoDataFrame
        A (mutating!) set of census blocks
    num_districts: int
        Total number of districts to divide the region into
    """
    district_count = 0
    region_mask = block_centroids["district"].notna()
    split_district(block_centroids, region_mask, num_districts, district_count)
