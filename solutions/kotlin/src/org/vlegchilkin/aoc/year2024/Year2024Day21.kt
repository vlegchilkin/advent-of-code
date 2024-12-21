package org.vlegchilkin.aoc.year2024

import org.vlegchilkin.aoc.*
import kotlin.math.abs


/**
 * 2024/21: Keypad Conundrum
 */
class Year2024Day21(input: String) : Solution {
  private val codes = input.toList { it }
  private val numericPad: Map<Char, C> =
    """
    789
    456
    123
    .0A 
    """.trimIndent().toCSpace().map { (pos, key) -> key to pos }.toMap()

  private val directionalPad: Map<Char, C> =
    """
    .^A
    <v> 
    """.trimIndent().toCSpace().map { (pos, key) -> key to pos }.toMap()

  private fun countTotalComplexity(numOfDirPads: Int): Long {
    val pads = buildList {
      add(numericPad)
      repeat(numOfDirPads) { add(directionalPad) }
    }

    val cache = Array(pads.size) { mutableMapOf<String, Long>() }
    fun dfs(code: String, index: Int): Long {
      if (index == pads.size) return code.length.toLong()
      cache[index][code]?.let { return it }

      val pad = pads[index]
      var result = 0L
      code.mapNotNull(pad::get).fold(pad['A']!!) { fromPos, toPos ->
        val (dy, dx) = toPos - fromPos
        val cy = (if (dy > 0) "v" else if (dy < 0) "^" else "").repeat(abs(dy))
        val cx = (if (dx > 0) ">" else if (dx < 0) "<" else "").repeat(abs(dx))
        result += minOf(
          if ((toPos.first to fromPos.second) in pad.values) dfs("$cy${cx}A", index + 1) else Long.MAX_VALUE,
          if ((fromPos.first to toPos.second) in pad.values) dfs("$cx${cy}A", index + 1) else Long.MAX_VALUE,
        )
        toPos
      }

      return result.also { cache[index][code] = it }
    }

    fun complexity(code: String): Long {
      val sequenceLength = dfs(code, 0)
      val numeric = code.takeWhile { it.isDigit() }.toLong()
      return sequenceLength * numeric
    }

    val result = codes.sumOf { complexity(it) }
    return result
  }

  override fun partA(): Long {
    return countTotalComplexity(2)
  }

  override fun partB(): Long {
    return countTotalComplexity(25)
  }

  companion object : Test(2024, 21, { Year2024Day21(it) })
}
