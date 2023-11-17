package org.vlegchilkin.aoc.year2020

import org.vlegchilkin.aoc.Test
import org.vlegchilkin.aoc.Solution
import org.vlegchilkin.aoc.trimSplitMap

class Year2020Day5(input: String) : Solution {
  private val seats = input.trimSplitMap {
    it.replace("B", "1")
      .replace("F", "0")
      .replace("R", "1")
      .replace("L", "0")
      .toInt(2)
  }


  override fun partA(): Any {
    return seats.max()
  }

  override fun partB(): Any {
    return seats.sorted().zipWithNext().first { (a, b) -> a + 1 != b }.first + 1
  }

  companion object : Test(2020, 5, { Year2020Day5(it) })
}