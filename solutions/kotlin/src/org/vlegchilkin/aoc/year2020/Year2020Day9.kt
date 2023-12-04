package org.vlegchilkin.aoc.year2020

import org.vlegchilkin.aoc.Solution
import org.vlegchilkin.aoc.Test
import org.vlegchilkin.aoc.toList

class Year2020Day9(input: String) : Solution {
  private val numbers = input.toList { it.toLong() }

  override fun partA(): Long {
    val window = numbers.subList(0, 25).toMutableSet()
    numbers.drop(25).forEachIndexed {  i, num ->
      window.firstOrNull { it * 2 < num && (num-it) in window } ?: return num
      window.remove(numbers[i])
      window.add(num)
    }
    throw IllegalArgumentException("There is no results for input provided")
  }

  override fun partB(): Any {
    val xmas = partA()
    var hi = 0
    var total = 0L
    for (lo in numbers.indices) {
      while (total < xmas) {
        total += numbers[hi++]
      }
      if (total == xmas) {
        val range = numbers.subList(lo, hi)
        return range.max() + range.min()
      }
      total -= numbers[lo]
    }
    throw IllegalArgumentException("There is no results for input provided")
  }

  companion object : Test(2020, 9, { Year2020Day9(it) })
}