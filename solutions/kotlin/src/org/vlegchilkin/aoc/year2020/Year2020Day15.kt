package org.vlegchilkin.aoc.year2020

import org.vlegchilkin.aoc.Test
import org.vlegchilkin.aoc.Solution
import org.vlegchilkin.aoc.trimSplitMap

class Year2020Day15(input: String) : Solution {
  private val numbers = input.trimSplitMap(",") { it.toInt() }

  private fun run(count: Int): Int {
    val cache = hashMapOf(*numbers.dropLast(1).mapIndexed { index, value -> value to index }.toTypedArray())
    var counter = numbers.size
    var last = numbers.last()
    do {
      (cache[last]?.let { counter - it - 1 } ?: 0).let {
        cache[last] = counter - 1
        last = it
      }
    }
    while (++counter < count)

    return last
  }

  override fun partA(): Int {
    return run(2020)
  }

  override fun partB(): Int {
    return run(30000000)
  }

  companion object : Test(2020, 15, { Year2020Day15(it) })
}