package org.vlegchilkin.aoc.year2020

import org.vlegchilkin.aoc.*

class Year2020Day14(input: String) : Solution {
  private val commands = input.toList { it.split(" = ").toPair() }

  fun <T> run(mask: (String) -> T, assignFunction: (Long, Long, T) -> Pair<List<Long>, Long>): Long {
    var m = mask("")
    val memory = mutableMapOf<Long, Long>()
    val pattern = """^mem\[(\d+)]$""".toRegex()
    commands.forEach { (cmd, arg) ->
      when (cmd) {
        "mask" -> m = mask(arg)
        else -> {
          val arg0 = pattern.matchEntire(cmd)!!.groupValues[1].toLong()
          assignFunction(arg0, arg.toLong(), m).let { (a, c) -> a.forEach { memory[it] = c } }
        }
      }
    }
    return memory.values.sum()
  }

  override fun partA(): Long {
    return run(mask = {
      it.fold(0L to 0L) { (set, clear), bit ->
        (set shl 1) + (bit == '1').toInt() to (clear shl 1) + (bit != '0').toInt()
      }
    }) { arg0, arg1, (set, clear) -> listOf(arg0) to ((arg1 or set) and clear) }
  }

  override fun partB(): Long {
    return run(mask = {
      it.foldIndexed(0L to mutableListOf<Long>()) { i, (setToOne, floatMasks), c ->
        if (c == 'X') floatMasks.add(1L shl (it.length - i - 1))
        (setToOne shl 1) + (c == '1').toInt() to floatMasks
      }
    }) { arg0, arg1, (setToOne, floatBits) ->
      fun generate(addr: Long, index: Int, addresses: MutableList<Long> = mutableListOf()): MutableList<Long> {
        if (index < floatBits.size) {
          generate(addr, index + 1, addresses)
          generate(
            addr + (if (addr and floatBits[index] == 0L) floatBits[index] else -floatBits[index]),
            index + 1,
            addresses
          )
        }
        else {
          addresses.add(addr)
        }
        return addresses
      }

      generate(arg0 or setToOne, 0) to arg1
    }
  }

  companion object : Test(2020, 14, { Year2020Day14(it) })
}