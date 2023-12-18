package org.vlegchilkin.aoc.year2023

import org.vlegchilkin.aoc.*
import kotlin.math.absoluteValue


/**
 * 2023/18: Lavaduct Lagoon
 */
class Year2023Day18(input: String) : Solution {
  data class Record(val cmd: Char, val steps: Int, val color: String)

  private val records = input.toList { it.split(' ').toObject(Record::class) }

  private fun fence(commands: List<Pair<Direction, Int>>): List<C> {
    var pos = 0 to 0
    val fence = mutableListOf(pos)
    commands.mapTo(fence) { (dir, steps) ->
      pos += dir * steps
      pos
    }
    return fence
  }

  private fun capacity(fence: List<C>): Long {
    val area = fence.area()
    val perimeter = fence.windowed(2).fold(0L) { acc, (a, b) ->
      acc + (a.first - b.first).absoluteValue + (a.second - b.second).absoluteValue
    }
    return area + perimeter / 2 + 1
  }

  override fun partA(): Any {
    val commands = records.map { Direction.of(it.cmd)!! to it.steps }
    return capacity(fence(commands))
  }

  override fun partB(): Any {
    fun parse(color: String): Pair<Direction, Int> {
      val data = color.removeSurrounding("(#", ")")
      val steps = data.dropLast(1).toInt(16)
      val direction = Direction.of("RDLU"[data.last() - '0'])!!
      return direction to steps
    }

    val commands = records.map { parse(it.color) }
    return capacity(fence(commands))
  }

  companion object : Test(2023, 18, { Year2023Day18(it) })
}
