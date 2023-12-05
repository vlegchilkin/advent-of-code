package org.vlegchilkin.aoc.year2023

import org.vlegchilkin.aoc.*

typealias Interval = Pair<Long, Long>
typealias Converter = Triple<Long, Long, Long>

/**
 * 2023/5: If You Give A Seed A Fertilizer
 */
class Year2023Day5(input: String) : Solution {
  private val soil: List<Long>
  private val transformers: List<List<Converter>>

  init {
    val data = input.toList("\n\n") { it.substringAfter(":") }
    soil = data[0].toLongList()
    transformers = data.drop(1).map { block -> block.toList { it.toLongList().toTriple() } }
  }

  override fun partA(): Any {
    fun dfs(num: Long, level: Int): Long {
      if (level == transformers.size) return num
      val converter = transformers[level].firstOrNull { (_, src, len) ->
        num in src..<src + len
      }
      val nextLevelNum = converter?.let { converter.first + (num - converter.second) } ?: num
      return dfs(nextLevelNum, level + 1)
    }

    return soil.minOf { dfs(it, 0) }
  }

  override fun partB(): Any {
    fun transform(interval: Interval, transformer: List<Converter>): List<Interval> {
      val result = mutableListOf<Interval>()
      val processed = mutableListOf<Interval>()

      transformer.forEach { (dst, src, len) ->
        val x = maxOf(interval.first, src)
        val y = minOf(interval.second, src + len)
        if (x < y) {
          result.add(dst + x - src to dst + y - src)
          processed.add(x to y)
        }
      }

      processed.sortBy { it.first }
      var x = interval.first
      for ((x0, x1) in processed) {
        if (x0 > x) result.add(x to x0)
        x = x1
      }
      if (interval.second > x) result.add(x to interval.second)
      return result
    }

    var intervals = soil.chunked(2).map { it[0] to it[0] + it[1] }
    for (transformer in transformers) {
      intervals = intervals.flatMap { transform(it, transformer) }
    }
    return intervals.minOf { it.first }
  }

  companion object : Test(2023, 5, { Year2023Day5(it) })
}
