package org.vlegchilkin.aoc.year2025

import org.vlegchilkin.aoc.*


/**
 * 2025/2: Gift Shop
 */
class Year2025Day2(input: String) : Solution {
  private val ranges = input.toList(",") { it.split("-").map(String::toLong).toPair() }

  override fun partA(): Any {
    val values = mutableSetOf<Long>()

    for ((a, b) in ranges) {
      for (c in a..b) {
        val x = c.toString().takeIf { it.length % 2 == 0 } ?: continue
        val d = x.length / 2
        if (x.substring(0, d) == x.substring(d)) values += c
      }
    }

    return values.sum()
  }

  override fun partB(): Any {
    val values = mutableSetOf<Long>()

    for ((a, b) in ranges) {
      for (c in a..b) {
        val x = c.toString()
        for (dx in 1..x.length / 2) {
          if (x.length % dx != 0) continue
          val chunked = x.chunked(dx)
          if (chunked.all { it == chunked[0] }) {
            values += c
            break
          }
        }
      }
    }

    return values.sum()
  }

  companion object : Test(2025, 2, { Year2025Day2(it) })
}
