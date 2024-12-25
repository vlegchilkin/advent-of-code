package org.vlegchilkin.aoc.year2024

import org.vlegchilkin.aoc.*


/**
 * 2024/25: Code Chronicle
 */
class Year2024Day25(input: String) : Solution {
  private val blocks = input.toList("\n\n") { block -> block.toList { it } }

  override fun partA(): Any {
    val (keyData, locksData) = blocks.partition { it[0][0] == '.' }
    val (n, m) = with(keyData[0]) { size to this[0].length }

    fun toNumeric(data: List<String>) = data.fold(IntArray(m) { 0 }) { acc, line ->
      line.forEachIndexed { index, c -> acc[index] += (c == '#').toInt() }
      acc
    }

    fun isFit(key: IntArray, lock: IntArray) = key.zip(lock).all { (a, b) -> a + b <= n }

    val keys = keyData.map { toNumeric(it) }
    val locks = locksData.map { toNumeric(it) }

    var counter = 0
    for (key in keys) for (lock in locks) counter += isFit(key, lock).toInt()
    return counter
  }

  override fun partB() = ""

  companion object : Test(2024, 25, { Year2024Day25(it) })
}
