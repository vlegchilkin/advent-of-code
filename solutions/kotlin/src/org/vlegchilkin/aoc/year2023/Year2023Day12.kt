package org.vlegchilkin.aoc.year2023

import org.vlegchilkin.aoc.*


/**
 * 2023/12: Hot Springs
 */
class Year2023Day12(input: String) : Solution {
  private val records = input.toList { line ->
    val (a, b) = line.split(' ')
    a to b.toIntList().toIntArray()
  }

  fun count(mask: CharArray, counters: IntArray): Long {
    val cache = mutableMapOf<Triple<Int, Int, Int>, Long>()
    fun dp(mi: Int, ci: Int, streak: Int): Long {
      val dpKey = Triple(mi, ci, streak)
      cache[dpKey]?.let { return it }

      if (ci == counters.size) return (mi..<mask.size).all { mask[it] in "?." }.toLong()
        .also { cache[dpKey] = it }
      if (mi == mask.size) return 0L
        .also { cache[dpKey] = 0L }

      fun logic(c: Char): Long {
        when (c) {
          '#' -> {
            if (streak == counters[ci]) return 0
            return dp(mi + 1, ci, streak + 1)
          }
          '.' -> {
            if (streak == 0) return dp(mi + 1, ci, streak)
            else {
              if (streak != counters[ci]) return 0
              return dp(mi + 1, ci + 1, 0)
            }
          }
          else -> throw IllegalArgumentException()
        }
      }

      return mask[mi].let {
        when (it) {
          '?' -> logic('.') + logic('#')
          else -> logic(it)
        }
      }.also { cache[dpKey] = it }
    }
    return dp(0, 0, 0)
  }

  override fun partA(): Long {
    return records.sumOf { (m, c) -> count("$m.".toCharArray(), c) }
  }

  override fun partB(): Long {
    return records.sumOf { (m, c) ->
      val mask = "$m?$m?$m?$m?$m.".toCharArray()
      val counters = buildList { repeat(5) { addAll(c.asSequence()) } }.toIntArray()
      count(mask, counters)
    }
  }


  companion object : Test(2023, 12, { Year2023Day12(it) })
}
