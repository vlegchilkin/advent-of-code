package org.vlegchilkin.aoc.year2024

import org.vlegchilkin.aoc.*


/**
 * 2024/11: Plutonian Pebbles
 */
class Year2024Day11(input: String) : Solution {
  private val stones = input.toLongList()

  private fun transform(num: Long): List<Long> {
    return when {
      num == 0L -> listOf(1L)
      num.toString().length % 2 == 0 -> {
        val x = "$num"
        val mid = x.length / 2
        listOf(x.substring(0, mid).toLong(), x.substring(mid).toLong())
      }
      else -> listOf(num * 2024)
    }
  }

  override fun partA(): Long {
    var current = ArrayList(stones).toList()
    for (step in 1..25) {
      current = current.flatMap { num -> transform(num) }
    }
    return current.size.toLong()
  }

  override fun partB(): Long {
    var current = stones.groupBy { it }.mapValues { it.value.size.toLong() }
    for (step in 1..75) {
      current = current.entries
        .flatMap { (num, stones) -> transform(num).map { it to stones } }
        .groupBy({ it.first }, { it.second })
        .mapValues { it.value.sum() }
    }
    return current.values.sum()
  }

  companion object : Test(2024, 11, { Year2024Day11(it) })
}
