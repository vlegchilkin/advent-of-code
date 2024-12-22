package org.vlegchilkin.aoc.year2024

import org.vlegchilkin.aoc.*


/**
 * 2024/22: Monkey Market
 */
class Year2024Day22(input: String) : Solution {
  private val initialSecrets = input.toLongList()
  private val patternSize = 4

  private fun Long.mixAndPrune(secret: Long) = (this xor secret) % 16777216
  private fun Long.nextSecret(steps: Int = 1): Long {
    var value = this
    repeat(steps) {
      value = value.mixAndPrune(value * 64)
      value = value.mixAndPrune(value / 32)
      value = value.mixAndPrune(value * 2048)
    }
    return value
  }

  data class Sequence(val bananas: List<Int>, val changes: List<Int>)

  override fun partAB(): Pair<Long, Int> {
    val sequences = initialSecrets.map { seed ->
      val bananas = generateSequence(seed) { it.nextSecret() }.take(2001).map { it.toInt() % 10 }.toList()
      val changes = bananas.zipWithNext().map { (a, b) -> b - a }
      Sequence(bananas, changes)
    }

    fun Sequence.findProfits(): Map<List<Int>, Int> {
      val result = mutableMapOf<List<Int>, Int>()
      for (start in 0..<changes.size - patternSize) {
        val pattern = changes.subList(start, start + patternSize)
        result.putIfAbsent(pattern, bananas[start + patternSize])
      }
      return result
    }

    val sequenceProfits = sequences.map { it.findProfits() }
    val possiblePatterns = sequenceProfits.flatMap { it.keys }.toSet()

    fun profit(pattern: List<Int>) = sequenceProfits.sumOf { profits -> profits[pattern] ?: 0 }

    val partA = initialSecrets.sumOf { it.nextSecret(2000) }
    val partB = possiblePatterns.maxOf { profit(it) }
    return partA to partB
  }

  companion object : Test(2024, 22, { Year2024Day22(it) })
}
