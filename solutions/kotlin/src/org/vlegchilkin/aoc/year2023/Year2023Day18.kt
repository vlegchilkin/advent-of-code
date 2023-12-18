package org.vlegchilkin.aoc.year2023

import org.vlegchilkin.aoc.*


/**
 * 2023/18: Lavaduct Lagoon
 */
class Year2023Day18(input: String) : Solution {
  data class Record(val cmd: Char, val steps: Int, val color: String)

  private val records = input.toList { it.split(' ').toObject(Record::class) }

  private fun capacity(fence: CPath): Long {
    return fence.area() + fence.length() / 2 + 1
  }

  override fun partA(): Any {
    val commands = records.map { Direction.of(it.cmd)!! to it.steps }
    return capacity(commands.toPath())
  }

  override fun partB(): Any {
    fun parse(color: String): Pair<Direction, Int> {
      val data = color.removeSurrounding("(#", ")")
      val steps = data.dropLast(1).toInt(16)
      val direction = Direction.of("RDLU"[data.last() - '0'])!!
      return direction to steps
    }

    val commands = records.map { parse(it.color) }
    return capacity(commands.toPath())
  }

  companion object : Test(2023, 18, { Year2023Day18(it) })
}
