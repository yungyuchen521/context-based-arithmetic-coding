### Arithmetic Encoding

<table>
  <tr>
    <th>ARGUMENTS</th>
    <th>DETAIL</th>
    <th>DEFAULT</th>
  </tr>
  <tr>
    <th>src</th>
    <td>File to be compressed</td>
    <td>Must be provided</td>
  </tr>
  <tr>
    <th>out</th>
    <td>Path of the output file</td>
    <td>"{src}.comp"</td>
  </tr>
  <tr>
    <th>mode</th>
    <td><strong>B</strong>: Treat the file as a byte sequence<br/><strong>b</strong>: Treat the file as a bit sequence</td>
    <td>Must be provided</td>
  </tr>
  <tr>
    <th>len</th>
    <td>Length of the lower & upper limit<br/>for integer implementation</td>
    <td>Must be provided</td>
  </tr>
</table>

#### Sample Commands
```shell script
# treat the file as a byte sequence
python arithmetic_encode.py src=alexnet.pth mode=B len=30
```
```shell script
# treat the file as a bit sequence
python arithmetic_encode.py src=alexnet.pth mode=b len=33
```

### Context-based Encoding

<table>
  <tr>
    <th>ARGUMENTS</th>
    <th>DETAIL</th>
    <th>DEFAULT</th>
  </tr>
  <tr>
    <th>src</th>
    <td>File to be compressed</td>
    <td>Must be provided</td>
  </tr>
  <tr>
    <th>out</th>
    <td>Path of the output file</td>
    <td>"{src}.comp"</td>
  </tr>
  <tr>
    <th>mode</th>
    <td>As in <strong>Arithmetic Encoding<strong/></td>
    <td>Must be provided</td>
  </tr>
  <tr>
    <th>len</th>
    <td>As in <strong>Arithmetic Encoding<strong/></td>
    <td>Must be provided</td>
  </tr>
  <tr>
    <th>method</th>
    <td><strong>A</strong>, <strong>B</strong>, or <strong>C</strong>.<br/>Method to set count for the escape symbol.<br/>Please refer to the report for more details.</td>
    <td>A</td>
  </tr>
  <tr>
    <th>exc</th>
    <td><strong>T</strong>: Apply Exclusion Principle.<br/><strong>F</strong>: Do not apply Exclusion Principle.</td>
    <td>F</td>
  </tr>
</table>

#### Sample Command
```shell script
# using Exclusion Principle & Method B
python context_based_encode.py src=alexnet.pth mode=B len=30 method=B exc=T
```
