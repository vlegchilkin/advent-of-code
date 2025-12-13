package org.vlegchilkin.aoc.year2025

import org.vlegchilkin.aoc.*


/**
* 2025/5: Cafeteria
*/
class Year2025Day5(input: String) : Solution {
  private val ranges: List<LongRange>
  private val ingredients: List<Long>

  init {
    val (rangesInp, ingredientsInp) = input.toList("\n\n") { block -> block.toList { it } }
    ranges = rangesInp.map { range ->
      range.split('-').map { it.toLong() }.toPair().let { LongRange(it.first, it.second) }
    }
    ingredients = ingredientsInp.map { it.toLong() }
  }

  override fun partA(): Any {
    return ingredients.count { id -> ranges.any { range -> id in range } }
  }

  override fun partB(): Any {
    return ranges.union().sumOf { range -> range.endInclusive - range.start + 1 }
  }

  companion object : Test(2025, 5, { Year2025Day5(it) })
}
