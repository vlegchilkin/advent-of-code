package org.vlegchilkin.aoc.year2020

import org.vlegchilkin.aoc.Test
import org.vlegchilkin.aoc.Solution
import org.vlegchilkin.aoc.toInt
import org.vlegchilkin.aoc.trimSplitMap

class Year2020Day3(input: String) : Solution {
  private val lines = input.trimSplitMap { it }

  private fun countTrees(right: Int, down: Int): Int {
    var counter = 0
    lines.forEachIndexed { row, line ->
      if (row % down == 0) {
        counter += (line[(row / down) * right % line.length] == '#').toInt()
      }
    }
    return counter
  }

  override fun partA(): Int {
    return countTrees(3, 1)
  }

  override fun partB(): Long {
    return listOf(1 to 1, 3 to 1, 5 to 1, 7 to 1, 1 to 2).map { (right, down) ->
      countTrees(right, down)
    }.fold(1L) { acc, i -> acc * i }
  }

  companion object : Test(2020, 3, { Year2020Day3(it) })
}